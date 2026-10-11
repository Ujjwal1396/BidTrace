"""
BidTrace Model A: Pre-Qualified Merkle Whitelist Engine
======================================================
Constructs deterministic sorted-pair Merkle Trees over approved bidder public keys
and generates inclusion proofs verifiable by Anchor smart contracts on Solana.
Supports both SHA-256 (Solana standard) and Keccak-256 (OpenZeppelin / EVM standard).
"""

import hashlib
from typing import List, Dict, Any, Optional, Union
from .crypto import to_32bytes, b58encode, b58decode


def keccak_256(data: bytes) -> bytes:
    """
    Pure Python zero-dependency Keccak-256 implementation (FIPS 202 Keccak-f[1600] permutation).
    Matches Ethereum keccak256, OpenZeppelin MerkleProof, and solana_program::keccak::hash syscall.
    Padding: pad10*1 with 0x01 ... 0x80 (distinct from NIST SHA3-256 which uses 0x06).
    """
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
    ]
    ROTC = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14],
    ]

    def rol64(x: int, n: int) -> int:
        return ((x << (n % 64)) | (x >> (64 - (n % 64)))) & 0xFFFFFFFFFFFFFFFF

    state = [[0] * 5 for _ in range(5)]
    rate = 136  # 1088 bits / 8

    padlen = rate - (len(data) % rate)
    if padlen == 1:
        padded = data + bytes([0x81])
    else:
        padded = data + bytes([0x01]) + bytes(padlen - 2) + bytes([0x80])

    for block_idx in range(0, len(padded), rate):
        block = padded[block_idx:block_idx + rate]
        for i in range(rate // 8):
            x = i % 5
            y = i // 5
            val = int.from_bytes(block[i * 8:(i + 1) * 8], "little")
            state[x][y] ^= val

        for round_idx in range(24):
            # Theta
            C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
            D = [C[(x - 1) % 5] ^ rol64(C[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    state[x][y] ^= D[x]

            # Rho and Pi
            B = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2 * x + 3 * y) % 5] = rol64(state[x][y], ROTC[x][y])

            # Chi
            for x in range(5):
                for y in range(5):
                    state[x][y] = (B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])) & 0xFFFFFFFFFFFFFFFF

            # Iota
            state[0][0] ^= RC[round_idx]

    out = bytearray()
    for i in range(4):  # 4 words = 32 bytes
        x = i % 5
        y = i // 5
        out += state[x][y].to_bytes(8, "little")
    return bytes(out)


def compute_leaf(bidder_key: Any, algorithm: str = "sha256") -> bytes:
    """
    Computes leaf hash for a bidder:
    - 'sha256': SHA-256(bidder_pubkey_32bytes)
    - 'keccak256': Keccak-256(bidder_pubkey_32bytes) (OpenZeppelin standard)
    Matches Anchor handle_commit_dual_bid instruction.
    """
    raw_key = to_32bytes(bidder_key)
    if algorithm.lower() in ("keccak", "keccak256", "keccak-256"):
        return keccak_256(raw_key)
    return hashlib.sha256(raw_key).digest()


def hash_pair(a: bytes, b: bytes, algorithm: str = "sha256") -> bytes:
    """
    Computes sorted-pair hash:
    if a <= b: H(a || b) else H(b || a).
    Supports 'sha256' and 'keccak256'.
    """
    first, second = (a, b) if a <= b else (b, a)
    data = first + second
    if algorithm.lower() in ("keccak", "keccak256", "keccak-256"):
        return keccak_256(data)
    return hashlib.sha256(data).digest()


def verify_merkle_proof(
    bidder_key: Any,
    proof: List[Union[bytes, str]],
    root: Union[bytes, str],
    algorithm: Optional[str] = None
) -> bool:
    """
    Verifies that a bidder belongs to the Merkle tree with the given root.
    Proof elements and root can be either 32-byte bytes or hex strings.
    If algorithm is None (default), checks both 'sha256' and 'keccak256',
    matching the on-chain dual-hash verification engine.
    """
    root_bytes = to_32bytes(root)
    algorithms = [algorithm] if algorithm else ["sha256", "keccak256"]

    for algo in algorithms:
        current = compute_leaf(bidder_key, algorithm=algo)
        for sib in proof:
            sib_bytes = to_32bytes(sib)
            current = hash_pair(current, sib_bytes, algorithm=algo)
        if current == root_bytes:
            return True
    return False


class MerkleTree:
    """
    A sorted-pair Merkle Tree for Model A Pre-Qualified Whitelisting.
    Supports both 'sha256' (Solana standard) and 'keccak256' (OpenZeppelin / EVM standard).
    """
    def __init__(self, bidders: List[Any], algorithm: str = "sha256"):
        if not bidders:
            raise ValueError("Cannot construct Merkle tree with empty bidder list")

        self.algorithm = algorithm.lower()
        self.raw_bidders = list(bidders)
        self.leaves: List[bytes] = [compute_leaf(b, algorithm=self.algorithm) for b in self.raw_bidders]
        self.levels: List[List[bytes]] = [self.leaves]
        self._build_tree()

    def _build_tree(self):
        current_level = self.leaves
        while len(current_level) > 1:
            next_level: List[bytes] = []
            n = len(current_level)
            for i in range(0, n, 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < n else left
                next_level.append(hash_pair(left, right, algorithm=self.algorithm))
            self.levels.append(next_level)
            current_level = next_level

    @property
    def root(self) -> bytes:
        return self.levels[-1][0] if self.levels else b"\x00" * 32

    @property
    def root_hex(self) -> str:
        return self.root.hex()

    def get_proof(self, bidder_key: Any) -> List[bytes]:
        """
        Returns list of 32-byte sibling hashes forming the inclusion proof.
        """
        target_leaf = compute_leaf(bidder_key, algorithm=self.algorithm)
        try:
            index = self.leaves.index(target_leaf)
        except ValueError:
            raise ValueError(f"Bidder key not found in Merkle tree leaves: {bidder_key}")

        proof: List[bytes] = []
        for level in self.levels[:-1]:
            is_right_child = (index % 2 == 1)
            sibling_index = index - 1 if is_right_child else index + 1
            if sibling_index < len(level):
                proof.append(level[sibling_index])
            else:
                # Odd length; paired with itself
                proof.append(level[index])
            index = index // 2

        return proof

    def get_proof_hex(self, bidder_key: Any) -> List[str]:
        """Returns proof as list of hex strings."""
        return [p.hex() for p in self.get_proof(bidder_key)]

    def to_dict(self) -> Dict[str, Any]:
        """Exports tree metadata for API responses and OCDS attachments."""
        return {
            "algorithm": self.algorithm,
            "root_hex": self.root_hex,
            "bidders_count": len(self.raw_bidders),
            "bidders": [
                {
                    "bidder": b if isinstance(b, str) else b.hex(),
                    "leaf_hex": compute_leaf(b, algorithm=self.algorithm).hex(),
                    "proof_hex": self.get_proof_hex(b)
                }
                for b in self.raw_bidders
            ]
        }
