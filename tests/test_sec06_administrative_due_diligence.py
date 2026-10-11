"""
SEC-06 Target 1 Test Suite: Administrative Due Diligence in Model B Open Tenders
==============================================================================
Validates:
1. Model B bids initialize in AdminStatus::Pending when admin_review_deadline_slot > submission_deadline_slot.
2. review_administrative_compliance is strictly gated to the AdministrativeReview phase and authority signer.
3. Slot boundary: reviews are rejected once admin_review_deadline_slot has elapsed.
4. Double review is prevented with AdminAlreadyReviewed.
5. Statutory rejection codes are immutably recorded for disqualified bidders.
6. Technical proposal reveal (Envelope A) strictly rejects unreviewed (Pending) and disqualified (Failed) bidders
   with BidderNotAdminPassed, eliminating premature unsealing.
7. REST API endpoint /api/bid/admin_review correctly records review decisions and statutory codes.
"""

import unittest
import hashlib
import secrets

from bidtrace_py.crypto import (
    generate_keypair,
    compute_tech_commitment,
    compute_fin_commitment,
)
from bidtrace_py.ledger import (
    BidTraceLedger,
    TenderStatus,
    TenderMode,
    EvaluationType,
    AdminStatus,
    BondMode,
)
from bidtrace_py.relayer import BidTraceRelayerGateway


class TestSEC06AdministrativeDueDiligence(unittest.TestCase):
    def setUp(self):
        self.ledger = BidTraceLedger()
        self.authority = generate_keypair()
        self.impostor = generate_keypair()

    def test_01_model_b_dual_bid_initializes_as_pending_admin_status(self):
        """
        Verify that in Model B open tenders with an explicit review window,
        committed bids initialize as AdminStatus.Pending and do not increment total_admin_passed.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-INIT-PENDING",
            tender_mode=TenderMode.PostQualifiedOpen,
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
            tech_eval_deadline_slot=1060,
            fin_reveal_deadline_slot=1080,
        )
        tender_pda = tender["pda"]

        bidder = generate_keypair()
        tech_comm = compute_tech_commitment(tender_pda, bidder["public_key"], "aa"*32, "PROP_HASH").hex()
        fin_comm = compute_fin_commitment(tender_pda, bidder["public_key"], "bb"*32, 5000000, "BOQ_HASH").hex()

        bid = self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="dd"*32,
            tech_commitment_hash=tech_comm,
            fin_commitment_hash=fin_comm,
        )

        self.assertEqual(bid["admin_status"], AdminStatus.Pending)
        self.assertEqual(bid["admin_rejection_code"], 0)
        self.assertEqual(self.ledger.tenders[tender_pda]["total_committed"], 1)
        self.assertEqual(self.ledger.tenders[tender_pda]["total_admin_passed"], 0)

    def test_02_admin_review_gated_to_administrative_review_phase(self):
        """
        Verify that review_administrative_compliance is rejected while in SubmissionsOpen
        and requires transitioning to AdministrativeReview.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-PHASE-GATE",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
        )
        tender_pda = tender["pda"]
        bidder = generate_keypair()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00"*32,
            tech_commitment_hash="11"*32,
            fin_commitment_hash="22"*32,
        )

        # Attempt to review while still in SubmissionsOpen
        with self.assertRaises(ValueError) as ctx:
            self.ledger.review_administrative_compliance(
                tender_pda=tender_pda,
                bidder_pubkey=bidder["public_key"],
                passed=True,
                authority_pubkey=self.authority["public_key"],
            )
        self.assertIn("TenderNotAdminReview", str(ctx.exception))

        # Advance past submission deadline to AdministrativeReview
        self.ledger.current_slot = 1021
        self.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])
        self.assertEqual(self.ledger.tenders[tender_pda]["status"], TenderStatus.AdministrativeReview)

        # Now review succeeds
        reviewed = self.ledger.review_administrative_compliance(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            passed=True,
            authority_pubkey=self.authority["public_key"],
        )
        self.assertEqual(reviewed["admin_status"], AdminStatus.Passed)
        self.assertEqual(self.ledger.tenders[tender_pda]["total_admin_passed"], 1)

    def test_03_admin_review_deadline_enforcement(self):
        """
        Verify that review_administrative_compliance is strictly rejected once
        the consensus slot exceeds admin_review_deadline_slot.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-DEADLINE",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
        )
        tender_pda = tender["pda"]
        bidder = generate_keypair()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00"*32,
            tech_commitment_hash="11"*32,
            fin_commitment_hash="22"*32,
        )

        self.ledger.current_slot = 1021
        self.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])

        # Exceed admin review deadline (1041 > 1040)
        self.ledger.current_slot = 1041
        with self.assertRaises(ValueError) as ctx:
            self.ledger.review_administrative_compliance(
                tender_pda=tender_pda,
                bidder_pubkey=bidder["public_key"],
                passed=True,
                authority_pubkey=self.authority["public_key"],
            )
        self.assertIn("AdminReviewDeadlineExceeded", str(ctx.exception))

    def test_04_double_admin_review_prevented(self):
        """
        Verify that a bidder already reviewed cannot have their evaluation overwritten.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-DOUBLE-REVIEW",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
        )
        tender_pda = tender["pda"]
        bidder = generate_keypair()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00"*32,
            tech_commitment_hash="11"*32,
            fin_commitment_hash="22"*32,
        )

        self.ledger.current_slot = 1025
        self.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])

        # Initial review: Pass
        self.ledger.review_administrative_compliance(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            passed=True,
            authority_pubkey=self.authority["public_key"],
        )

        # Duplicate review attempt
        with self.assertRaises(ValueError) as ctx:
            self.ledger.review_administrative_compliance(
                tender_pda=tender_pda,
                bidder_pubkey=bidder["public_key"],
                passed=False,
                rejection_code=101,
                authority_pubkey=self.authority["public_key"],
            )
        self.assertIn("AdminAlreadyReviewed", str(ctx.exception))

    def test_05_unauthorized_authority_rejected(self):
        """
        Verify that only the certified tender authority can submit compliance determinations.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-UNAUTH-AUTHORITY",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
        )
        tender_pda = tender["pda"]
        bidder = generate_keypair()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00"*32,
            tech_commitment_hash="11"*32,
            fin_commitment_hash="22"*32,
        )

        self.ledger.current_slot = 1025
        self.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])

        with self.assertRaises(ValueError) as ctx:
            self.ledger.review_administrative_compliance(
                tender_pda=tender_pda,
                bidder_pubkey=bidder["public_key"],
                passed=True,
                authority_pubkey=self.impostor["public_key"],
            )
        self.assertIn("UnauthorizedAuthority", str(ctx.exception))

    def test_06_unreviewed_and_failed_bidders_strictly_blocked_from_revealing_technical_bid(self):
        """
        Primary SEC-06 Remediation Verification:
        1. Bidder A passes administrative review -> Envelope A unsealing succeeds.
        2. Bidder B fails administrative review (e.g. rejection code 403: Invalid Tax Clearance)
           -> Envelope A unsealing is strictly rejected with BidderNotAdminPassed.
        3. Bidder C is never reviewed (Pending)
           -> Envelope A unsealing is strictly rejected with BidderNotAdminPassed.
        """
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-ENVELOPE-A-GATE",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
            tech_eval_deadline_slot=1060,
            fin_reveal_deadline_slot=1080,
        )
        tender_pda = tender["pda"]

        # 3 Bidders
        bidder_a = generate_keypair() # Approved
        bidder_b = generate_keypair() # Rejected
        bidder_c = generate_keypair() # Unreviewed / Pending

        salt_a = secrets.token_hex(32)
        prop_a = hashlib.sha256(b"PROPOSAL_A").hexdigest()
        comm_a = compute_tech_commitment(tender_pda, bidder_a["public_key"], salt_a, prop_a).hex()

        salt_b = secrets.token_hex(32)
        prop_b = hashlib.sha256(b"PROPOSAL_B").hexdigest()
        comm_b = compute_tech_commitment(tender_pda, bidder_b["public_key"], salt_b, prop_b).hex()

        salt_c = secrets.token_hex(32)
        prop_c = hashlib.sha256(b"PROPOSAL_C").hexdigest()
        comm_c = compute_tech_commitment(tender_pda, bidder_c["public_key"], salt_c, prop_c).hex()

        self.ledger.commit_dual_bid(tender_pda, bidder_a["public_key"], "00"*32, comm_a, "11"*32)
        self.ledger.commit_dual_bid(tender_pda, bidder_b["public_key"], "00"*32, comm_b, "22"*32)
        self.ledger.commit_dual_bid(tender_pda, bidder_c["public_key"], "00"*32, comm_c, "33"*32)

        # Transition to AdministrativeReview
        self.ledger.current_slot = 1025
        self.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])
        self.assertEqual(self.ledger.tenders[tender_pda]["status"], TenderStatus.AdministrativeReview)

        # Review Bidder A: Passed
        self.ledger.review_administrative_compliance(
            tender_pda=tender_pda,
            bidder_pubkey=bidder_a["public_key"],
            passed=True,
            authority_pubkey=self.authority["public_key"],
        )

        # Review Bidder B: Failed (Code 403: Missing ISO Clearance)
        self.ledger.review_administrative_compliance(
            tender_pda=tender_pda,
            bidder_pubkey=bidder_b["public_key"],
            passed=False,
            rejection_code=403,
            authority_pubkey=self.authority["public_key"],
        )

        # Bidder C remains unreviewed (Pending)

        # Transition to TechnicalEvaluation without auto-approving pending bids
        self.ledger.current_slot = 1045
        self.ledger.advance_tender_phase(
            tender_pda,
            caller_pubkey=self.authority["public_key"],
            auto_approve_pending=False
        )
        self.assertEqual(self.ledger.tenders[tender_pda]["status"], TenderStatus.TechnicalEvaluation)

        # Verification 1: Disqualified Bidder B is BLOCKED from unsealing technical proposal
        with self.assertRaises(ValueError) as ctx_b:
            self.ledger.reveal_technical_bid(tender_pda, bidder_b["public_key"], salt_b, prop_b)
        self.assertIn("BidderNotAdminPassed", str(ctx_b.exception))

        # Verification 2: Unreviewed Bidder C is BLOCKED from unsealing technical proposal
        with self.assertRaises(ValueError) as ctx_c:
            self.ledger.reveal_technical_bid(tender_pda, bidder_c["public_key"], salt_c, prop_c)
        self.assertIn("BidderNotAdminPassed", str(ctx_c.exception))

        # Verification 3: Approved Bidder A successfully unseals Envelope A
        revealed_a = self.ledger.reveal_technical_bid(tender_pda, bidder_a["public_key"], salt_a, prop_a)
        self.assertTrue(revealed_a["is_tech_revealed"])

    def test_07_relayer_gateway_admin_review_integration(self):
        """
        Verify that BidTraceRelayerGateway correctly wraps review_administrative_compliance
        and exposes signed receipts.
        """
        relayer = BidTraceRelayerGateway()
        tender = relayer.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC06-RELAYER",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1040,
        )
        tender_pda = tender["pda"]
        bidder = generate_keypair()
        relayer.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00"*32,
            tech_commitment_hash="11"*32,
            fin_commitment_hash="22"*32,
        )

        relayer.ledger.current_slot = 1025
        relayer.ledger.advance_tender_phase(tender_pda, caller_pubkey=self.authority["public_key"])

        res = relayer.review_administrative_compliance(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            passed=False,
            rejection_code=502,
            authority_pubkey=self.authority["public_key"],
        )

        self.assertEqual(res["bid"]["admin_status"], AdminStatus.Failed)
        self.assertEqual(res["bid"]["admin_rejection_code"], 502)
        self.assertTrue(res["tx_signature"].startswith("tx_admin_review_"))


if __name__ == "__main__":
    unittest.main()
