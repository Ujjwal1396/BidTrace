"""
SEC-07 Target 2 Test Suite: Double Finalization Guard & Total Qualified Drift Prevention
=======================================================================================
Validates:
1. finalize_technical_scores sets is_tech_finalized=True on DualBidCommitment.
2. Second invocation on an already finalized bidder strictly reverts with TechnicalScoreAlreadyFinalized.
3. Total qualified counter (tender.total_tech_qualified) remains strictly accurate and immune to drift.
4. Double finalization on technically disqualified bidders is also strictly rejected.
5. Unauthorized authority signer is rejected with UnauthorizedAuthority.
6. Unrevealed technical proposals cannot be finalized (TechNotRevealed).
7. Non-TechnicalEvaluation tender status is rejected (TenderNotTechnicalEvaluation).
8. REST API /api/tender/finalize_technical rejects duplicate finalization requests (400 Bad Request).
9. Anti-lockout gate integrity: total_fin_revealed == total_tech_qualified is reliably satisfied.
"""

import unittest
import os
import json
import secrets
import hashlib
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer

from bidtrace_py.crypto import (
    generate_keypair,
    compute_tech_commitment,
    compute_fin_commitment,
    compute_grade_commitment,
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
from server import BidTraceHandler, state


class TestSEC07DoubleFinalizationGuard(unittest.TestCase):
    def setUp(self):
        self.ledger = BidTraceLedger()
        self.ledger.current_slot = 1000
        self.authority = generate_keypair()
        self.impostor = generate_keypair()

    def _setup_tender_in_tech_eval(self, evaluator_count: int = 5, min_tech_score_bps: int = 7500):
        evaluators = [generate_keypair()["public_key"] for _ in range(evaluator_count)]
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id=f"TENDER-SEC07-{secrets.token_hex(4)}",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1020,
            tech_eval_deadline_slot=1050,
            fin_reveal_deadline_slot=1070,
            min_tech_score_bps=min_tech_score_bps,
        )
        tender_pda = tender["pda"]

        self.ledger.initialize_committee(
            tender_pda=tender_pda,
            authority_pubkey=self.authority["public_key"],
            evaluators=evaluators,
            max_variance_bps=2000,
        )

        bidder = generate_keypair()
        tech_comm = compute_tech_commitment(tender_pda, bidder["public_key"], "00" * 32, "PROP_HASH").hex()
        fin_comm = compute_fin_commitment(tender_pda, bidder["public_key"], "11" * 32, 5000000, "BOQ_HASH").hex()

        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00" * 32,
            tech_commitment_hash=tech_comm,
            fin_commitment_hash=fin_comm,
        )

        # Advance to TechnicalEvaluation
        self.ledger.current_slot = 1030
        self.ledger.tenders[tender_pda]["status"] = TenderStatus.TechnicalEvaluation

        # Reveal technical bid
        self.ledger.reveal_technical_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            salt_tech="00" * 32,
            proposal_hash="PROP_HASH",
        )

        return tender_pda, evaluators, bidder

    def test_01_successful_finalization_sets_is_tech_finalized_and_increments_qualified(self):
        """
        Verify that first finalization successfully calculates Olympic trimmed mean,
        marks is_tech_finalized=True, and increments tender.total_tech_qualified.
        """
        tender_pda, evaluators, bidder = self._setup_tender_in_tech_eval(evaluator_count=5, min_tech_score_bps=7500)

        for ev in evaluators:
            comm = compute_grade_commitment(tender_pda, bidder["public_key"], ev, "00" * 32, [1600] * 5, "00" * 32).hex()
            self.ledger.commit_evaluator_grade(tender_pda, ev, bidder["public_key"], comm)
            self.ledger.reveal_evaluator_grade(tender_pda, ev, bidder["public_key"], [1600] * 5, "00" * 32, "00" * 32)

        res = self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertEqual(res["final_score_bps"], 8000)
        self.assertTrue(res["is_tech_qualified"])

        bid_pda = self.ledger.derive_bid_pda(tender_pda, bidder["public_key"])
        bid = self.ledger.commitments[bid_pda]
        self.assertTrue(bid["is_tech_finalized"])
        self.assertTrue(bid["is_tech_qualified"])
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 1)

    def test_02_double_finalization_strictly_blocked_preventing_total_qualified_drift(self):
        """
        Primary Target 2 Verification:
        Re-invoking finalize_technical_scores on an already finalized bidder MUST be strictly
        rejected with TechnicalScoreAlreadyFinalized, and tender.total_tech_qualified MUST NOT drift.
        """
        tender_pda, evaluators, bidder = self._setup_tender_in_tech_eval(evaluator_count=5, min_tech_score_bps=7500)

        for ev in evaluators:
            comm = compute_grade_commitment(tender_pda, bidder["public_key"], ev, "00" * 32, [1600] * 5, "00" * 32).hex()
            self.ledger.commit_evaluator_grade(tender_pda, ev, bidder["public_key"], comm)
            self.ledger.reveal_evaluator_grade(tender_pda, ev, bidder["public_key"], [1600] * 5, "00" * 32, "00" * 32)

        # 1. Initial finalization
        self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 1)

        # 2. Duplicate finalization attempt
        with self.assertRaises(ValueError) as ctx:
            self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertIn("TechnicalScoreAlreadyFinalized", str(ctx.exception))

        # 3. Third duplicate finalization attempt
        with self.assertRaises(ValueError) as ctx2:
            self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertIn("TechnicalScoreAlreadyFinalized", str(ctx2.exception))

        # Invariant check: counter must remain strictly 1, eliminating drift
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 1)

    def test_03_double_finalization_blocked_on_disqualified_bidder(self):
        """
        Verify that double finalization protection applies equally to technically disqualified bids,
        preventing re-evaluation tampering.
        """
        tender_pda, evaluators, bidder = self._setup_tender_in_tech_eval(evaluator_count=5, min_tech_score_bps=7500)

        # Disqualified scores (5000 bps < 7500 bps)
        for ev in evaluators:
            comm = compute_grade_commitment(tender_pda, bidder["public_key"], ev, "00" * 32, [1000] * 5, "00" * 32).hex()
            self.ledger.commit_evaluator_grade(tender_pda, ev, bidder["public_key"], comm)
            self.ledger.reveal_evaluator_grade(tender_pda, ev, bidder["public_key"], [1000] * 5, "00" * 32, "00" * 32)

        res = self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertEqual(res["final_score_bps"], 5000)
        self.assertFalse(res["is_tech_qualified"])

        bid_pda = self.ledger.derive_bid_pda(tender_pda, bidder["public_key"])
        bid = self.ledger.commitments[bid_pda]
        self.assertTrue(bid["is_tech_finalized"])
        self.assertFalse(bid["is_tech_qualified"])
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 0)

        # Duplicate attempt on disqualified bidder
        with self.assertRaises(ValueError) as ctx:
            self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertIn("TechnicalScoreAlreadyFinalized", str(ctx.exception))
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 0)

    def test_04_unauthorized_authority_rejected(self):
        """
        Verify that only the certified tender authority signer can finalize technical scores.
        """
        tender_pda, evaluators, bidder = self._setup_tender_in_tech_eval(evaluator_count=5)

        for ev in evaluators:
            comm = compute_grade_commitment(tender_pda, bidder["public_key"], ev, "00" * 32, [1600] * 5, "00" * 32).hex()
            self.ledger.commit_evaluator_grade(tender_pda, ev, bidder["public_key"], comm)
            self.ledger.reveal_evaluator_grade(tender_pda, ev, bidder["public_key"], [1600] * 5, "00" * 32, "00" * 32)

        with self.assertRaises(ValueError) as ctx:
            self.ledger.finalize_technical_scores(tender_pda, self.impostor["public_key"], bidder["public_key"])
        self.assertIn("UnauthorizedAuthority", str(ctx.exception))

    def test_05_unrevealed_technical_proposal_cannot_be_finalized(self):
        """
        Verify that finalization rejects bids whose technical proposal (Envelope A)
        has not been unsealed yet.
        """
        evaluators = [generate_keypair()["public_key"] for _ in range(3)]
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC07-UNREVEALED",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1020,
            tech_eval_deadline_slot=1050,
            fin_reveal_deadline_slot=1070,
        )
        tender_pda = tender["pda"]
        self.ledger.initialize_committee(
            tender_pda=tender_pda,
            authority_pubkey=self.authority["public_key"],
            evaluators=evaluators,
            max_variance_bps=2000,
        )

        bidder = generate_keypair()
        tech_comm = compute_tech_commitment(tender_pda, bidder["public_key"], "00" * 32, "PROP_HASH").hex()
        fin_comm = compute_fin_commitment(tender_pda, bidder["public_key"], "11" * 32, 5000000, "BOQ_HASH").hex()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00" * 32,
            tech_commitment_hash=tech_comm,
            fin_commitment_hash=fin_comm,
        )

        # Advance to TechnicalEvaluation but DO NOT unseal Envelope A
        self.ledger.current_slot = 1030
        self.ledger.tenders[tender_pda]["status"] = TenderStatus.TechnicalEvaluation

        with self.assertRaises(ValueError) as ctx:
            self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertIn("TechNotRevealed", str(ctx.exception))

    def test_06_tender_not_in_technical_evaluation_rejected(self):
        """
        Verify that finalization is strictly gated to the TechnicalEvaluation state machine phase.
        """
        evaluators = [generate_keypair()["public_key"] for _ in range(3)]
        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority["public_key"],
            tender_id="TENDER-SEC07-WRONG-PHASE",
            submission_deadline_slot=1020,
            admin_review_deadline_slot=1020,
            tech_eval_deadline_slot=1050,
            fin_reveal_deadline_slot=1070,
        )
        tender_pda = tender["pda"]
        self.ledger.initialize_committee(
            tender_pda=tender_pda,
            authority_pubkey=self.authority["public_key"],
            evaluators=evaluators,
            max_variance_bps=2000,
        )

        bidder = generate_keypair()
        self.ledger.commit_dual_bid(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            admin_dossier_hash="00" * 32,
            tech_commitment_hash="11" * 32,
            fin_commitment_hash="22" * 32,
        )

        # Still in SubmissionsOpen
        with self.assertRaises(ValueError) as ctx:
            self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertIn("TenderNotTechnicalEvaluation", str(ctx.exception))

    def test_07_anti_lockout_gate_integrity_preserved(self):
        """
        Verify end-to-end anti-lockout gate integrity:
        Without drift, total_tech_qualified is exactly 1. When the qualified bidder reveals
        their financial envelope, total_fin_revealed == total_tech_qualified is true (1 == 1),
        allowing legitimate award without artificial delay.
        """
        tender_pda, evaluators, bidder = self._setup_tender_in_tech_eval(evaluator_count=5, min_tech_score_bps=7500)

        for ev in evaluators:
            comm = compute_grade_commitment(tender_pda, bidder["public_key"], ev, "00" * 32, [1600] * 5, "00" * 32).hex()
            self.ledger.commit_evaluator_grade(tender_pda, ev, bidder["public_key"], comm)
            self.ledger.reveal_evaluator_grade(tender_pda, ev, bidder["public_key"], [1600] * 5, "00" * 32, "00" * 32)

        # Finalize technical score
        self.ledger.finalize_technical_scores(tender_pda, self.authority["public_key"], bidder["public_key"])
        self.assertEqual(self.ledger.tenders[tender_pda]["total_tech_qualified"], 1)

        # Advance to FinancialEvaluation
        self.ledger.current_slot = 1055
        self.ledger.tenders[tender_pda]["status"] = TenderStatus.FinancialEvaluation

        # Unseal financial envelope
        self.ledger.reveal_financial_envelope(
            tender_pda=tender_pda,
            bidder_pubkey=bidder["public_key"],
            salt_fin="11" * 32,
            price=5000000,
            boq_hash="BOQ_HASH",
        )

        tender = self.ledger.tenders[tender_pda]
        self.assertEqual(tender["total_fin_revealed"], 1)
        self.assertEqual(tender["total_tech_qualified"], 1)
        # Anti-lockout condition: total_fin_revealed == total_tech_qualified
        self.assertTrue(tender["total_fin_revealed"] == tender["total_tech_qualified"])


class TestSEC07RestApiParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_port = 8107
        cls.server_address = f"http://127.0.0.1:{cls.server_port}"
        state.reset()

        cls.httpd = HTTPServer(("127.0.0.1", cls.server_port), BidTraceHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _post(self, path, payload):
        req = urllib.request.Request(
            f"{self.server_address}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode("utf-8"))

    def test_08_rest_api_duplicate_finalization_returns_400_and_guards_counter(self):
        """
        Verify that /api/tender/finalize_technical rejects duplicate invocation with 400 Bad Request,
        preventing API-level total_qualified drift.
        """
        self._post("/api/reset", {})

        # 1. Create tender
        t_res = self._post("/api/tender/create", {
            "tender_id": "TENDER-API-SEC07",
            "submission_deadline_slot": 1020,
            "admin_review_deadline_slot": 1020,
            "tech_eval_deadline_slot": 1050,
            "fin_reveal_deadline_slot": 1070,
            "evaluators": ["ev1", "ev2", "ev3"],
            "max_variance_bps": 2000,
            "min_tech_score_bps": 7500,
        })
        self.assertEqual(t_res[0], 200)

        # 2. Register bidder
        bidder = generate_keypair()
        tech_comm = compute_tech_commitment(state.tender_pda, bidder["public_key"], "00" * 32, "PROP_HASH").hex()
        fin_comm = compute_fin_commitment(state.tender_pda, bidder["public_key"], "11" * 32, 5000000, "BOQ_HASH").hex()

        b_res = self._post("/api/bid/commit_dual", {
            "bidder_pubkey": bidder["public_key"],
            "admin_dossier_hash": "00" * 32,
            "tech_commitment_hash": tech_comm,
            "fin_commitment_hash": fin_comm,
        })
        self.assertEqual(b_res[0], 200)

        # 3. Administrative clearance and Advance to TechnicalEvaluation
        bid_pda = state.ledger.derive_bid_pda(state.tender_pda, bidder["public_key"])
        state.ledger.commitments[bid_pda]["admin_status"] = AdminStatus.Passed
        state.ledger.current_slot = 1030
        state.ledger.tenders[state.tender_pda]["status"] = TenderStatus.TechnicalEvaluation

        # 4. Reveal technical bid
        r_res = self._post("/api/bid/reveal_technical", {
            "bidder_pubkey": bidder["public_key"],
            "salt_tech": "00" * 32,
            "proposal_hash": "PROP_HASH",
        })
        self.assertEqual(r_res[0], 200)

        # 5. Evaluators submit & reveal grades
        for ev in ["ev1", "ev2", "ev3"]:
            comm = compute_grade_commitment(state.tender_pda, bidder["public_key"], ev, "00" * 32, [1600] * 5, "00" * 32).hex()
            self._post("/api/evaluator/commit_grade", {
                "evaluator_pubkey": ev,
                "bidder_pubkey": bidder["public_key"],
                "commitment_hash": comm,
            })
            self._post("/api/evaluator/reveal_grade", {
                "evaluator_pubkey": ev,
                "bidder_pubkey": bidder["public_key"],
                "sub_scores": [1600] * 5,
                "salt": "00" * 32,
                "justification_hash": "00" * 32,
            })

        # 6. First API finalization -> 200 OK
        f1_code, f1_data = self._post("/api/tender/finalize_technical", {
            "bidder_pubkeys": [bidder["public_key"]]
        })
        self.assertEqual(f1_code, 200)
        self.assertEqual(f1_data["total_qualified"], 1)
        self.assertEqual(state.ledger.tenders[state.tender_pda]["total_tech_qualified"], 1)

        # 7. Second API finalization attempt -> 400 Bad Request
        f2_code, f2_data = self._post("/api/tender/finalize_technical", {
            "bidder_pubkeys": [bidder["public_key"]]
        })
        self.assertEqual(f2_code, 400)
        self.assertIn("TechnicalScoreAlreadyFinalized", f2_data["message"])

        # Counter must remain strictly 1
        self.assertEqual(state.ledger.tenders[state.tender_pda]["total_tech_qualified"], 1)


if __name__ == "__main__":
    unittest.main()
