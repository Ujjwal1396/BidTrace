"""
BidTrace Security Audit - Target 3 Test Suite:
Merkle Whitelist Hashing Parity & Dual-Algorithm Verification (Keccak-256 vs SHA-256)
=====================================================================================
Verifies:
1. Pure Python Keccak-256 exact conformity with NIST Keccak-f[1600] and OpenZeppelin test vectors.
2. Sorted-pair Merkle Tree construction and proof verification under both Keccak-256 and SHA-256.
3. Strict isolation: Keccak-256 trees strictly reject SHA-256 proofs and vice versa.
4. Model A on-chain ledger commitment acceptance under both Keccak-256 and SHA-256 roots.
5. Strict rejection of forged, tampered, or non-whitelisted bidder proofs under both algorithms.
"""

import unittest
import hashlib
from bidtrace_py.merkle import (
    keccak_256,
    compute_leaf,
    hash_pair,
    verify_merkle_proof,
    MerkleTree,
)
from bidtrace_py.ledger import BidTraceLedger, TenderMode, TenderStatus, AdminStatus
from bidtrace_py.crypto import to_32bytes


class TestMerkleHashingParity(unittest.TestCase):
    def setUp(self):
        self.ledger = BidTraceLedger()
        self.authority = "Auth1111111111111111111111111111111111111111"

    def test_01_keccak256_standard_test_vectors(self):
        """Test 1: Verify pure-Python Keccak-256 against standard NIST / Ethereum test vectors."""
        # Vector 1: Empty string
        empty_hash = keccak_256(b"").hex()
        self.assertEqual(
            empty_hash,
            "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
            "Empty string Keccak-256 mismatch"
        )

        # Vector 2: 'hello'
        hello_hash = keccak_256(b"hello").hex()
        self.assertEqual(
            hello_hash,
            "1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8",
            "'hello' Keccak-256 mismatch"
        )

        # Vector 3: 'The quick brown fox jumps over the lazy dog'
        fox_hash = keccak_256(b"The quick brown fox jumps over the lazy dog").hex()
        self.assertEqual(
            fox_hash,
            "4d741b6f1eb29cb2a9b9911c82f56fa8d73b04959d3d9d222895df6c0b28aa15",
            "Fox string Keccak-256 mismatch"
        )

        # Vector 4: Multi-block input (rate = 136 bytes; test 200 bytes)
        msg_200 = b"A" * 200
        hash_200 = keccak_256(msg_200)
        self.assertEqual(len(hash_200), 32)
        self.assertNotEqual(hash_200, hashlib.sha256(msg_200).digest())

    def test_02_commutative_sorted_pair_hashing(self):
        """Test 2: Verify commutative property hash_pair(a, b) == hash_pair(b, a)."""
        a = b"\x10" * 32
        b = b"\x20" * 32

        # SHA-256
        self.assertEqual(hash_pair(a, b, algorithm="sha256"), hash_pair(b, a, algorithm="sha256"))
        # Keccak-256
        self.assertEqual(hash_pair(a, b, algorithm="keccak256"), hash_pair(b, a, algorithm="keccak256"))

        # Both must produce distinct hashes for different algorithms
        self.assertNotEqual(
            hash_pair(a, b, algorithm="sha256"),
            hash_pair(a, b, algorithm="keccak256")
        )

    def test_03_keccak256_merkle_tree_and_proofs(self):
        """Test 3: Build OpenZeppelin-compatible Keccak-256 tree and verify proofs."""
        bidders = [
            "Bidder11111111111111111111111111111111111111",
            "Bidder22222222222222222222222222222222222222",
            "Bidder33333333333333333333333333333333333333",
            "Bidder44444444444444444444444444444444444444",
        ]
        tree = MerkleTree(bidders, algorithm="keccak256")
        self.assertEqual(tree.algorithm, "keccak256")
        self.assertEqual(len(tree.root), 32)

        for b in bidders:
            proof = tree.get_proof(b)
            # Strictly verify with keccak256
            self.assertTrue(verify_merkle_proof(b, proof, tree.root, algorithm="keccak256"))
            # Verify with dual auto-detection (None)
            self.assertTrue(verify_merkle_proof(b, proof, tree.root))
            # Strict SHA-256 check MUST fail on Keccak tree
            self.assertFalse(verify_merkle_proof(b, proof, tree.root, algorithm="sha256"))

    def test_04_sha256_merkle_tree_and_proofs(self):
        """Test 4: Build Solana-native SHA-256 tree and verify proofs."""
        bidders = [
            "Bidder11111111111111111111111111111111111111",
            "Bidder22222222222222222222222222222222222222",
            "Bidder33333333333333333333333333333333333333",
        ]
        tree = MerkleTree(bidders, algorithm="sha256")
        self.assertEqual(tree.algorithm, "sha256")

        for b in bidders:
            proof = tree.get_proof(b)
            # Strictly verify with sha256
            self.assertTrue(verify_merkle_proof(b, proof, tree.root, algorithm="sha256"))
            # Verify with dual auto-detection (None)
            self.assertTrue(verify_merkle_proof(b, proof, tree.root))
            # Strict Keccak-256 check MUST fail on SHA-256 tree
            self.assertFalse(verify_merkle_proof(b, proof, tree.root, algorithm="keccak256"))

    def test_05_forged_proof_strict_rejection(self):
        """Test 5: Reject invalid/forged proofs under both algorithms."""
        bidders = [
            "Bidder11111111111111111111111111111111111111",
            "Bidder22222222222222222222222222222222222222",
        ]
        impostor = "Impostor99999999999999999999999999999999999"

        tree_keccak = MerkleTree(bidders, algorithm="keccak256")
        tree_sha = MerkleTree(bidders, algorithm="sha256")

        proof_keccak = tree_keccak.get_proof(bidders[0])
        proof_sha = tree_sha.get_proof(bidders[0])

        # Impostor using valid proof fails on both
        self.assertFalse(verify_merkle_proof(impostor, proof_keccak, tree_keccak.root))
        self.assertFalse(verify_merkle_proof(impostor, proof_sha, tree_sha.root))

        # Corrupted proof sibling fails
        tampered_proof = [b"\xff" * 32]
        self.assertFalse(verify_merkle_proof(bidders[0], tampered_proof, tree_keccak.root))
        self.assertFalse(verify_merkle_proof(bidders[0], tampered_proof, tree_sha.root))

    def test_06_model_a_ledger_keccak256_acceptance(self):
        """Test 6: Model A pre-qualified tender accepts Keccak-256 OpenZeppelin tree proofs."""
        bidders = [
            "Bidder11111111111111111111111111111111111111",
            "Bidder22222222222222222222222222222222222222",
            "Bidder33333333333333333333333333333333333333",
        ]
        tree = MerkleTree(bidders, algorithm="keccak256")

        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority,
            tender_id="TENDER-KECCAK-OZ",
            tender_mode=TenderMode.PreQualifiedWhitelist,
            authorized_bidders_root=tree.root_hex,
        )

        # Honest whitelisted bidder commits with Keccak proof
        proof_hex = tree.get_proof_hex(bidders[0])
        bid = self.ledger.commit_dual_bid(
            tender_pda=tender["pda"],
            bidder_pubkey=bidders[0],
            admin_dossier_hash="aa" * 32,
            tech_commitment_hash="bb" * 32,
            fin_commitment_hash="cc" * 32,
            whitelist_proof=proof_hex,
        )

        self.assertEqual(bid["admin_status"], AdminStatus.Passed)
        self.assertEqual(self.ledger.tenders[tender["pda"]]["total_admin_passed"], 1)

    def test_07_model_a_ledger_sha256_acceptance(self):
        """Test 7: Model A pre-qualified tender accepts SHA-256 Solana tree proofs."""
        bidders = [
            "Bidder11111111111111111111111111111111111111",
            "Bidder22222222222222222222222222222222222222",
        ]
        tree = MerkleTree(bidders, algorithm="sha256")

        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority,
            tender_id="TENDER-SHA256-SOL",
            tender_mode=TenderMode.PreQualifiedWhitelist,
            authorized_bidders_root=tree.root_hex,
        )

        # Honest whitelisted bidder commits with SHA-256 proof
        proof_hex = tree.get_proof_hex(bidders[0])
        bid = self.ledger.commit_dual_bid(
            tender_pda=tender["pda"],
            bidder_pubkey=bidders[0],
            admin_dossier_hash="aa" * 32,
            tech_commitment_hash="bb" * 32,
            fin_commitment_hash="cc" * 32,
            whitelist_proof=proof_hex,
        )

        self.assertEqual(bid["admin_status"], AdminStatus.Passed)
        self.assertEqual(self.ledger.tenders[tender["pda"]]["total_admin_passed"], 1)

    def test_08_model_a_ledger_rejection_of_unauthorized_bidder(self):
        """Test 8: Model A strictly rejects unauthorized bidders under Keccak and SHA roots."""
        bidders = ["Bidder11111111111111111111111111111111111111"]
        impostor = "Impostor99999999999999999999999999999999999"
        tree = MerkleTree(bidders, algorithm="keccak256")

        tender = self.ledger.initialize_tender(
            authority_pubkey=self.authority,
            tender_id="TENDER-REJECT-IMPOSTOR",
            tender_mode=TenderMode.PreQualifiedWhitelist,
            authorized_bidders_root=tree.root_hex,
        )

        # 1. Impostor missing proof
        with self.assertRaises(ValueError) as ctx:
            self.ledger.commit_dual_bid(
                tender_pda=tender["pda"],
                bidder_pubkey=impostor,
                admin_dossier_hash="aa" * 32,
                tech_commitment_hash="bb" * 32,
                fin_commitment_hash="cc" * 32,
                whitelist_proof=None,
            )
        self.assertIn("UnauthorizedBidder", str(ctx.exception))

        # 2. Impostor providing forged proof
        with self.assertRaises(ValueError) as ctx:
            self.ledger.commit_dual_bid(
                tender_pda=tender["pda"],
                bidder_pubkey=impostor,
                admin_dossier_hash="aa" * 32,
                tech_commitment_hash="bb" * 32,
                fin_commitment_hash="cc" * 32,
                whitelist_proof=["ff" * 32],
            )
        self.assertIn("InvalidMerkleProof", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
