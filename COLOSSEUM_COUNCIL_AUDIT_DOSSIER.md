# BidTrace 3.0: Complete System Specification, Source Code & Venture Vetting Dossier
## For Colosseum Hackathon Copilot & LLM Security Council Evaluation

**Project Name:** BidTrace 3.0  
**Repository:** [https://github.com/Ujjwal1396/BidTrace.git](https://github.com/Ujjwal1396/BidTrace.git) (`main` branch)  
**Latest Audit Commit:** `8d5a43b` (Targets 1, 2, and 3 fully resolved & verified)  
**Solana Devnet Program ID:** `x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ`  
**Devnet ProgramData Address:** `31T65nDyKp5Jyok1AE4YsCLH1nxEbnGWVBqvZjtf9iYp`  
**Deployer / Fee Payer Authority:** `GFRRqHMPekLkEUPDzwLXnBoETUU1EFrfFoZxiCWUwSzU`  
**Standards Implemented:** Solana Runtime (Anchor v0.30.1), Open Contracting Data Standard (OCDS 1.1), RFC 8785 JSON Canonicalization Scheme (JCS), OpenZeppelin Merkle Proof Standard.

---

## Table of Contents
1. [Executive Summary & Hackathon Thesis](#1-executive-summary--hackathon-thesis)
2. [The Real-World Procurement Crisis & Threat Model](#2-the-real-world-procurement-crisis--threat-model)
3. [System Architecture: Semantic Plane vs Consensus Plane](#3-system-architecture-semantic-plane-vs-consensus-plane)
4. [Mathematical & Cryptographic Invariants](#4-mathematical--cryptographic-invariants)
   - 4.1 Temporal Consensus Slot State Machine
   - 4.2 Olympic Trimmed Mean & Median Variance Filter
   - 4.3 The Commercial Secrecy Invariant
   - 4.4 Dual-Hash Merkle Verification (Keccak-256 & SHA-256)
   - 4.5 Anti-Arbitrary Winner Verification (QCBS Composite Scoring)
   - 4.6 Anti-Lockout Gates
   - 4.7 Double Finalization & Counter Drift Guard
5. [Complete Unabridged Rust Smart Contract Codebase](#5-complete-unabridged-rust-smart-contract-codebase)
   - 5.1 `Cargo.toml`
   - 5.2 `programs/bidtrace/src/lib.rs`
   - 5.3 `programs/bidtrace/src/state.rs`
   - 5.4 `programs/bidtrace/src/errors.rs`
   - 5.5 `instructions/initialize_tender.rs`
   - 5.6 `instructions/initialize_committee.rs`
   - 5.7 `instructions/commit_dual_bid.rs`
   - 5.8 `instructions/advance_tender_phase.rs`
   - 5.9 `instructions/review_administrative_compliance.rs`
   - 5.10 `instructions/reveal_technical_bid.rs`
   - 5.11 `instructions/commit_evaluator_grade.rs`
   - 5.12 `instructions/reveal_evaluator_grade.rs`
   - 5.13 `instructions/finalize_technical_scores.rs`
   - 5.14 `instructions/reveal_financial_envelope.rs`
   - 5.15 `instructions/record_award_qcbs.rs`
   - 5.16 `instructions/refund_disqualified_bond.rs`
6. [Off-Chain Reference Engine & REST Gateway](#6-off-chain-reference-engine--rest-gateway)
   - 6.1 `bidtrace_py/ledger.py` (Consensus Mirror)
   - 6.2 `bidtrace_py/merkle.py` (Dual Keccak/SHA Merkle Engine)
   - 6.3 `bidtrace_py/bonds.py` (Hybrid Bond Engine)
   - 6.4 `bidtrace_py/ocds.py` (RFC 8785 JCS Canonicalization)
   - 6.5 `server.py` (Gas-Sponsored Relayer Gateway)
7. [Comprehensive Test Suites & Verification Proofs](#7-comprehensive-test-suites--verification-proofs)
   - 7.1 Anchor Localnet Integration Tests (`14 / 14 Passing`)
   - 7.2 Python Unit & Integration Tests (`78 / 78 Passing`)
   - 7.3 Cross-Language RFC 8785 Hash Parity Proof
8. [Adversarial Attack Defense Matrix (10 Security Targets Verified)](#8-adversarial-attack-defense-matrix)
9. [Colosseum Hackathon & Venture Evaluation Rubric Alignment](#9-colosseum-hackathon--venture-evaluation-rubric-alignment)
10. [Unit Economics & GTM Strategy](#10-unit-economics--gtm-strategy)

---

## 1. Executive Summary & Hackathon Thesis

### 1.1 The $13 Trillion Global Public Procurement Crisis
Public and enterprise procurement represents **$13 Trillion USD annually** (15% to 20% of global GDP), spanning multilateral development banks (World Bank, Asian Development Bank, UN), national ministries of transport and energy, and private mega-EPC engineering conglomerates (Bechtel, VINCI, Fluor, Skanska).

According to the UN Office on Drugs and Crime (UNODC) and the World Bank Stolen Asset Recovery Initiative:
- Between **20% and 25% of public procurement expenditure is lost annually to corruption, kickbacks, and bid-rigging** (over $1.5 Trillion per year).
- The single most catastrophic structural vulnerability across all e-procurement systems (e-GP portals, SAP Ariba, Oracle Cloud ERP) is **The Post-Deadline Insider Exploitation Window**: the interval between the submission cutoff and the formal public opening.
- During this window, an insider holding database administrator (`sa` or `postgres` root) credentials can observe competing submissions, extract the lowest compliant price, and retroactively backdate a favored contractor's bid or substitute an altered technical proposal prior to the opening ceremony.
- When an honest bidder challenges the outcome in administrative court, the procurement agency produces internal database logs and states: *"That is what our authoritative database recorded."*

### 1.2 The BidTrace Solution
**BidTrace 3.0** replaces institutional trust and vulnerable centralized databases with an **incorruptible, mathematically verifiable cryptographic state machine** deployed on **Solana**:

1. **Strict Temporal Consensus Deadlines:** Enforced on Solana consensus slots (`Clock::get()?.slot`). Late bids cannot be injected by database administrators, corrupt ministers, or network operators.
2. **Two-Envelope Cryptographic Commit-Reveal:** Bidders commit `Envelope A` (Technical Proposal) and `Envelope B` (Financial Quotation) simultaneously as salted preimages before the submission deadline.
3. **The Commercial Secrecy Invariant:** If a contractor fails technical qualification ($S_{\text{tech}} < \text{Threshold}$), the smart contract **permanently locks Envelope B on-chain**. Competitors and buyers cannot extract their proprietary unit pricing or trade secrets. Disqualified bidders reclaim escrowed bonds via `refund_disqualified_bond` without ever unsealing Envelope B.
4. **On-Chain Olympic Trimmed Mean Scoring:** Evaluators commit blinded sub-scores. Scores differing from the committee median by more than `max_variance_bps` (with a 100 bps floor) are dynamically flagged (`is_outlier_flagged = true`). In 5-member committees, the single highest and lowest scores plus flagged outliers are automatically dropped.
5. **Anti-Arbitrary Winner Verification (QCBS):** Authority cannot award an inferior bidder. The contract programmatically evaluates all competing unsealed bids in `remaining_accounts` and reverts if the designated winner has an inferior Quality- and Cost-Based Selection (QCBS) composite score.
6. **Dual-Hash Merkle Whitelist Parity:** Private Mega-EPC pre-qualification (Model A) supports both **OpenZeppelin / EVM-standard Keccak-256** and **Solana-native SHA-256** sorted-pair Merkle proofs.
7. **The Fiat-to-Gas Decoupling:** Corporate buyers and subcontractors interact via fiat invoices, standard REST APIs, and PDF dossiers without holding SOL, managing private keys, or acquiring crypto assets. A gas-sponsored relayer pays transaction fees and submits cryptographic proofs to Solana.

---

## 2. The Real-World Procurement Crisis & Threat Model

| Real-World Threat Vector | Attack Scenario | Traditional IT Vulnerability | BidTrace Cryptographic Defense |
| :--- | :--- | :--- | :--- |
| **Late Bid Injection** | Corrupt minister inserts favored bidder's proposal 2 hours after cutoff. | Database admin updates MySQL `created_at` timestamp. | `Clock::get()?.slot <= submission_deadline_slot`. Consensus slots cannot be backdated. |
| **Bid Substitution** | Agency swaps technical blueprints after inspecting competitors. | Files overwritten in cloud S3 bucket. | Salted SHA-256 preimages verified against immutable `tech_commitment_hash`. |
| **Price Tampering** | Bidder claims verbal price was $3.5M instead of submitted $4.0M. | He-said-she-said arbitration. | `price` and `salt_fin` validated against on-chain `fin_commitment_hash`. |
| **Evaluator Bribery** | Corrupt panel member awards 98% to inflate favored bidder. | Evaluator average is distorted. | Olympic Trimmed Mean drops max score; automatically flags outlier (`is_outlier_flagged = true`). |
| **Commercial Secrecy Breach** | Agency leaks disqualified bidder's unit margins to favored competitor. | PDF opened on administrative intranet. | On-chain gate `bid.is_tech_qualified == true` prevents financial reveal forever. |
| **Early Award Lockout** | Corrupt buyer awards tender before honest bidders can reveal. | Buyer rushes paper decree. | Anti-lockout gate: `slot > fin_reveal_deadline_slot \|\| total_fin_revealed == total_tech_qualified`. |
| **Arbitrary Winner Selection** | Buyer selects 2nd-place bidder claiming "executive prerogative". | Uncontestable administrative fiat. | On-chain comparison against all competing bids in `record_award_qcbs`. |
| **Double Finalization Drift** | Authority re-finalizes bidder to manipulate `total_tech_qualified`. | Re-running API increments qualified count, altering quorum. | Dedicated `is_tech_finalized` boolean flag + account constraint `!bid.is_tech_finalized`. |
| **Merkle Whitelist Fraud** | Unauthorized bidder submits forged credentials. | Forged certificate PDF accepted by clerk. | On-chain dual Keccak-256 / SHA-256 sorted-pair Merkle proof verification. |
| **Tampered Tender Notice** | Agency changes evaluation rubrics retroactively. | Web page silently edited. | RFC 8785 Canonical JCS hash in `Tender` PDA must match notice exactly. |

---

## 3. System Architecture: Semantic Plane vs Consensus Plane

BidTrace decouples the procurement lifecycle into two synergistic planes:

```
+-----------------------------------------------------------------------------------+
|                           1. SEMANTIC PLANE (Off-Chain)                           |
|  - Open Contracting Data Standard (OCDS 1.1) JSON Releases                        |
|  - RFC 8785 JSON Canonicalization Scheme (JCS) Deterministic Hashing              |
|  - Standalone Air-Gapped Tribunal Dossier & Offline Verifier CLI                  |
|  - Hybrid Bond Formats (TradFi Surety, MT760 SWIFT, World Bank Debarment BSD)     |
+---------------------------------------------------------+-------------------------+
                                                          | Cryptographic Hash Anchor
                                                          v
+-----------------------------------------------------------------------------------+
|                          2. CONSENSUS PLANE (Solana On-Chain)                     |
|  - Program ID: x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ (Anchor 0.30.1)        |
|  - State Machine: SubmissionsOpen -> AdminReview -> TechEval -> FinEval -> Awarded|
|  - Temporal Slot Enforcement (Clock::get()?.slot)                                  |
|  - Two-Envelope Commit-Reveal: DualBidCommitment PDAs                             |
|  - Blinded Evaluator Grade Commitments & Olympic Trimmed Mean Outlier Filter      |
|  - Commercial Secrecy Enforcer: Permanent Financial Lockout for Disqualified Bids  |
|  - Anti-Arbitrary Winner Verification (Programmatic QCBS Formula)                 |
+-----------------------------------------------------------------------------------+
```

---

## 4. Mathematical & Cryptographic Invariants

### 4.1 Temporal Consensus Slot State Machine
Every tender enforces strictly sequential Solana slot boundaries:
$$\text{Current Slot} < \text{Slot}_{\text{sub}} \le \text{Slot}_{\text{admin}} \le \text{Slot}_{\text{tech}} \le \text{Slot}_{\text{fin}}$$

Phase transitions via `advance_tender_phase` require consensus time verification:
- `SubmissionsOpen` $\rightarrow$ `AdministrativeReview`: requires $\text{Slot} > \text{Slot}_{\text{sub}}$
- `AdministrativeReview` $\rightarrow$ `TechnicalEvaluation`: requires $\text{Slot} > \text{Slot}_{\text{admin}}$
- `TechnicalEvaluation` $\rightarrow$ `FinancialEvaluation`: requires $\text{Slot} > \text{Slot}_{\text{tech}}$

### 4.2 Olympic Trimmed Mean & Median Variance Filter
For an accredited evaluator panel of $N$ certified evaluators ($N \ge 3$):
1. **Median Determination:** Sort revealed scores $s_1 \le s_2 \le \dots \le s_N$:
   $$\text{Median} = \begin{cases} s_{(N+1)/2} & \text{if } N \text{ is odd} \\ \frac{s_{N/2} + s_{N/2 + 1}}{2} & \text{if } N \text{ is even} \end{cases}$$
2. **Outlier Threshold:**
   $$\Delta_{\max} = \max\left(100, \frac{\text{Median} \times \text{MaxVarianceBps}}{10000}\right)$$
   Scores where $|s_i - \text{Median}| > \Delta_{\max}$ are flagged as outliers (`is_outlier_flagged = true`).
3. **Olympic Trimming ($N \ge 4$):**
   Drop the single highest score ($s_N$), the single lowest score ($s_1$), and any remaining scores violating $\Delta_{\max}$:
   $$S_{\text{trimmed}} = \{ s_i \mid i \in [2, N-1] \text{ and } |s_i - \text{Median}| \le \Delta_{\max} \}$$
   $$\text{Final Technical Score} = \frac{1}{|S_{\text{trimmed}}|} \sum_{s \in S_{\text{trimmed}}} s$$
   If all scores are dropped due to extreme polarization, the contract reverts with `EmptyTrimmedScorePool`.

### 4.3 The Commercial Secrecy Invariant
Let $C_i$ be contractor $i$'s `DualBidCommitment`.
$$\text{Envelope A Unsealed} \iff C_i.\text{admin\_status} == \text{Passed}$$
$$\text{Envelope B Unsealed} \iff C_i.\text{is\_tech\_qualified} == \text{True}$$
If $C_i.\text{technical\_score\_bps} < \text{Tender}.\text{min\_tech\_score\_bps}$, then $C_i.\text{is\_tech\_qualified} = \text{False}$.
Any call to `reveal_financial_envelope` reverts with:
`BidTraceError::BidderTechnicallyDisqualified (6018)`

### 4.4 Dual-Hash Merkle Verification (Keccak-256 & SHA-256)
Model A Private Whitelist supports both OpenZeppelin / EVM and Solana-native Merkle roots:
$$\text{Verify}(P, R, K) = \text{Verify}_{\text{Keccak}}(P, R, K) \lor \text{Verify}_{\text{SHA256}}(P, R, K)$$
Where sorted-pair folding satisfies:
$$H_{\text{pair}}(a, b) = \begin{cases} H(a \parallel b) & \text{if } a \le b \\ H(b \parallel a) & \text{if } b < a \end{cases}$$

### 4.5 Anti-Arbitrary Winner Verification (QCBS Composite Scoring)
Under Quality- and Cost-Based Selection (QCBS):
$$S_{\text{composite}}(i) = \left(\frac{S_{\text{tech}}(i) \times W_{\text{tech}}}{10000}\right) + \left(\frac{P_{\min} \times 10000}{P(i)} \times \frac{W_{\text{fin}}}{10000}\right)$$
Where $W_{\text{tech}} + W_{\text{fin}} = 10000$ basis points (100%).
In `record_award_qcbs`, the authority must pass all competing revealed qualified bids in `remaining_accounts`. The contract computes $S_{\text{composite}}$ for each competing bid and strictly asserts:
$$S_{\text{composite}}(\text{Winner}) \ge S_{\text{composite}}(\text{Competing}_j) \quad \forall j$$
Reverting with `WinnerNotHighestCompositeScore (6023)` if an inferior contractor is selected.

### 4.6 Anti-Lockout Gates
Tender award is programmatically blocked while honest qualified contractors can still reveal:
$$\text{Award Permitted} \iff \text{Slot} > \text{Slot}_{\text{fin}} \lor \text{total\_fin\_revealed} == \text{total\_tech\_qualified}$$
Reverting with `FinancialRevealWindowActive (6024)`.

### 4.7 Double Finalization & Counter Drift Guard
Technical scoring for a bidder can be executed exactly once:
```rust
constraint = !bid_commitment.is_tech_finalized @ BidTraceError::TechnicalScoreAlreadyFinalized
```
Sets `bid_commitment.is_tech_finalized = true`. Increments `tender.total_tech_qualified` by 1 if and only if qualified, preventing re-evaluation manipulation of anti-lockout thresholds.

---

## 5. Complete Unabridged Rust Smart Contract Codebase

### 5.1 `programs/bidtrace/Cargo.toml`
```toml
[package]
name = "bidtrace"
version = "0.1.0"
description = "BidTrace - Incorruptible Cryptographic Deadline-Lock for Procurement"
edition = "2021"

[lib]
crate-type = ["cdylib", "lib"]
name = "bidtrace"

[features]
no-entrypoint = []
no-idl = []
no-log-ix-name = []
cpi = ["no-entrypoint"]
default = []
idl-build = ["anchor-lang/idl-build"]

[dependencies]
anchor-lang = { version = "0.30.1", features = ["init-if-needed"] }
solana-program = "=1.18.26"
sha2 = "0.10.8"
```

### 5.2 `programs/bidtrace/src/lib.rs`
```rust
use anchor_lang::prelude::*;

pub mod errors;
pub mod instructions;
pub mod state;

use instructions::*;
use state::{BondMode, EvaluationType, TenderMode};

declare_id!("x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ");

#[program]
pub mod bidtrace {
    use super::*;

    /// 1. Initialize a two-envelope tender with temporal slot deadlines, OCDS notice hash, and scoring parameters
    pub fn initialize_tender(
        ctx: Context<InitializeTender>,
        tender_id: String,
        ocds_notice_hash: [u8; 32],
        tender_mode: TenderMode,
        evaluation_type: EvaluationType,
        submission_deadline_slot: u64,
        admin_review_deadline_slot: u64,
        tech_eval_deadline_slot: u64,
        fin_reveal_deadline_slot: u64,
        authorized_bidders_root: [u8; 32],
        min_tech_score_bps: u16,
        tech_weight_bps: u16,
        fin_weight_bps: u16,
    ) -> Result<()> {
        instructions::initialize_tender::handle_initialize_tender(
            ctx,
            tender_id,
            ocds_notice_hash,
            tender_mode,
            evaluation_type,
            submission_deadline_slot,
            admin_review_deadline_slot,
            tech_eval_deadline_slot,
            fin_reveal_deadline_slot,
            authorized_bidders_root,
            min_tech_score_bps,
            tech_weight_bps,
            fin_weight_bps,
        )
    }

    /// 2. Initialize the evaluation committee with certified evaluators and outlier variance threshold
    pub fn initialize_committee(
        ctx: Context<InitializeCommittee>,
        evaluators: Vec<Pubkey>,
        max_variance_bps: u16,
    ) -> Result<()> {
        instructions::initialize_committee::handle_initialize_committee(
            ctx,
            evaluators,
            max_variance_bps,
        )
    }

    /// 3. Bidder commits a dual-envelope cryptographic proposal (Envelope A + Envelope B)
    pub fn commit_dual_bid(
        ctx: Context<CommitDualBid>,
        admin_dossier_hash: [u8; 32],
        tech_commitment_hash: [u8; 32],
        fin_commitment_hash: [u8; 32],
        bond_mode: BondMode,
        bond_amount: u64,
        whitelist_proof: Option<Vec<[u8; 32]>>,
    ) -> Result<()> {
        instructions::commit_dual_bid::handle_commit_dual_bid(
            ctx,
            admin_dossier_hash,
            tech_commitment_hash,
            fin_commitment_hash,
            bond_mode,
            bond_amount,
            whitelist_proof,
        )
    }

    /// 4. Advance tender phase based on temporal consensus slot deadlines
    pub fn advance_tender_phase(ctx: Context<AdvanceTenderPhase>) -> Result<()> {
        instructions::advance_tender_phase::handle_advance_tender_phase(ctx)
    }

    /// 5. Unseal Envelope A: Reveal technical proposal specification and blueprints
    pub fn reveal_technical_bid(
        ctx: Context<RevealTechnicalBid>,
        salt_tech: [u8; 32],
        proposal_hash: [u8; 32],
    ) -> Result<()> {
        instructions::reveal_technical_bid::handle_reveal_technical_bid(
            ctx,
            salt_tech,
            proposal_hash,
        )
    }

    /// 6. Evaluator commits a blinded cryptographic score across 5 sub-criteria
    pub fn commit_evaluator_grade(
        ctx: Context<CommitEvaluatorGrade>,
        commitment_hash: [u8; 32],
    ) -> Result<()> {
        instructions::commit_evaluator_grade::handle_commit_evaluator_grade(
            ctx,
            commitment_hash,
        )
    }

    /// 7. Evaluator reveals sub-scores and justification report hash
    pub fn reveal_evaluator_grade(
        ctx: Context<RevealEvaluatorGrade>,
        sub_scores: [u16; 5],
        salt: [u8; 32],
        justification_hash: [u8; 32],
    ) -> Result<()> {
        instructions::reveal_evaluator_grade::handle_reveal_evaluator_grade(
            ctx,
            sub_scores,
            salt,
            justification_hash,
        )
    }

    /// 8. Finalize technical scores using the on-chain Olympic Trimmed Mean and outlier rejection filter
    pub fn finalize_technical_scores<'info>(
        ctx: Context<'_, '_, '_, 'info, FinalizeTechnicalScores<'info>>,
    ) -> Result<()> {
        instructions::finalize_technical_scores::handle_finalize_technical_scores(ctx)
    }

    /// 9. Unseal Envelope B: Strictly gated to technically qualified bidders (Commercial Secrecy Invariant)
    pub fn reveal_financial_envelope(
        ctx: Context<RevealFinancialEnvelope>,
        salt_fin: [u8; 32],
        price: u64,
        boq_hash: [u8; 32],
    ) -> Result<()> {
        instructions::reveal_financial_envelope::handle_reveal_financial_envelope(
            ctx,
            salt_fin,
            price,
            boq_hash,
        )
    }

    /// 10. Record tender award with programmatic QCBS composite scoring formula
    pub fn record_award_qcbs<'info>(
        ctx: Context<'_, '_, '_, 'info, RecordAwardQcbs<'info>>,
        rationale_hash: [u8; 32],
    ) -> Result<()> {
        instructions::record_award_qcbs::handle_record_award_qcbs(ctx, rationale_hash)
    }

    /// 11. Refund escrowed bond to technically disqualified bidder without unsealing Envelope B
    pub fn refund_disqualified_bond(ctx: Context<RefundDisqualifiedBond>) -> Result<()> {
        instructions::refund_disqualified_bond::handle_refund_disqualified_bond(ctx)
    }

    /// 12. Evaluate administrative compliance for a committed bidder during AdministrativeReview phase
    pub fn review_administrative_compliance(
        ctx: Context<ReviewAdministrativeCompliance>,
        passed: bool,
        rejection_code: u16,
    ) -> Result<()> {
        instructions::review_administrative_compliance::handle_review_administrative_compliance(
            ctx,
            passed,
            rejection_code,
        )
    }
}
```

### 5.3 `programs/bidtrace/src/state.rs`
```rust
use anchor_lang::prelude::*;

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Debug)]
pub enum TenderStatus {
    SubmissionsOpen = 0,
    AdministrativeReview = 1,
    TechnicalEvaluation = 2,
    FinancialEvaluation = 3,
    Awarded = 4,
    Cancelled = 5,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum TenderMode {
    PreQualifiedWhitelist = 0, // Model A (Private EPCs / Merkle Root)
    PostQualifiedOpen = 1,     // Model B (World Bank / Bond Escrow)
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum EvaluationType {
    LeastCost = 0,
    QCBS = 1,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum AdminStatus {
    Pending = 0,
    Passed = 1,
    Failed = 2,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum BondMode {
    SolanaEscrow = 0,
    SuretyService = 1,
    BankGuaranteeAttestation = 2,
    BidSecuringDeclaration = 3,
}

#[account]
pub struct Tender {
    /// The procurement authority who created the tender
    pub authority: Pubkey,
    /// Unique human/system tender identifier (max 32 ASCII chars)
    pub tender_id: String,
    /// Canonical RFC 8785 SHA-256 hash of the OCDS 1.1 Tender Release notice
    pub ocds_notice_hash: [u8; 32],
    /// Mode: Pre-qualified whitelist (Model A) or Post-qualified open (Model B)
    pub tender_mode: TenderMode,
    /// Evaluation scoring formula: LeastCost or QCBS
    pub evaluation_type: EvaluationType,
    /// Current state machine status
    pub status: TenderStatus,

    // Temporal Slot Boundaries (Solana Consensus Time)
    pub submission_deadline_slot: u64,
    pub admin_review_deadline_slot: u64,
    pub tech_eval_deadline_slot: u64,
    pub fin_reveal_deadline_slot: u64,

    /// Merkle root of pre-authorized bidders (Model A; [0; 32] for open tender)
    pub authorized_bidders_root: [u8; 32],

    // Two-Envelope Scoring Parameters (Basis points: 10,000 = 100.00%)
    pub min_tech_score_bps: u16,  // Cutoff threshold (e.g. 7500 = 75.00%)
    pub tech_weight_bps: u16,     // Technical weight (e.g. 7000 = 70.00%)
    pub fin_weight_bps: u16,      // Financial weight (e.g. 3000 = 30.00%)

    // Progress Counters
    pub total_committed: u32,
    pub total_admin_passed: u32,
    pub total_tech_qualified: u32,
    pub total_fin_revealed: u32,

    // Pricing & Award Tracking
    pub lowest_revealed_price: u64,
    pub highest_composite_score: u64,
    pub winning_bidder: Option<Pubkey>,
    pub bump: u8,
}

impl Tender {
    pub const LEN: usize = 8 + 32 + (4 + 32) + 32 + 1 + 1 + 1 + 32 + 32 + 6 + 16 + 16 + 33 + 1 + 64;
}

#[account]
pub struct DualBidCommitment {
    /// Reference to the parent Tender PDA
    pub tender: Pubkey,
    /// Public key of the bidder
    pub bidder: Pubkey,
    /// Solana slot when the dual commitment was recorded
    pub committed_at_slot: u64,

    // Cryptographic Hashes
    pub admin_dossier_hash: [u8; 32],
    pub tech_commitment_hash: [u8; 32],
    pub fin_commitment_hash: [u8; 32],

    // Phase 1: Administrative Due Diligence
    pub admin_status: AdminStatus,
    pub admin_rejection_code: u16,

    // Phase 2: Technical Merit Scoring
    pub is_tech_revealed: bool,
    pub is_tech_finalized: bool,
    pub technical_score_bps: u16,
    pub is_tech_qualified: bool,

    // Phase 3: Financial Unsealing & Scoring
    pub is_fin_revealed: bool,
    pub revealed_price: u64,
    pub composite_score: u64,

    // Bond & Security Escrow
    pub bond_mode: BondMode,
    pub bond_amount: u64,
    pub is_bond_settled: bool,
    pub bump: u8,
}

impl DualBidCommitment {
    pub const LEN: usize = 8 + 32 + 32 + 8 + 96 + 3 + 5 + 17 + 11 + 64;
}

#[account]
pub struct TenderCommittee {
    pub tender: Pubkey,
    pub evaluators: Vec<Pubkey>,
    pub max_variance_bps: u16,
    pub is_locked: bool,
    pub bump: u8,
}

impl TenderCommittee {
    pub const LEN: usize = 8 + 32 + (4 + 32 * 10) + 2 + 1 + 1 + 64;
}

#[account]
pub struct EvaluatorGrade {
    pub tender: Pubkey,
    pub evaluator: Pubkey,
    pub bidder: Pubkey,
    pub commitment_hash: [u8; 32],
    pub committed_at_slot: u64,
    pub is_revealed: bool,
    pub sub_scores: [u16; 5],
    pub total_score_bps: u16,
    pub justification_hash: [u8; 32],
    pub is_outlier_flagged: bool,
    pub bump: u8,
}

impl EvaluatorGrade {
    pub const LEN: usize = 8 + 32 + 32 + 32 + 32 + 8 + 1 + 10 + 2 + 32 + 1 + 1 + 32;
}
```

### 5.4 `programs/bidtrace/src/errors.rs`
```rust
use anchor_lang::prelude::*;

#[error_code]
pub enum BidTraceError {
    #[msg("Submission deadline slot must be in the future.")]
    InvalidSubmissionDeadline, // 6000

    #[msg("Deadline slots must be strictly sequential (submission <= admin <= tech <= fin).")]
    InvalidDeadlineSequence, // 6001

    #[msg("Submission deadline has passed. Commitments are frozen.")]
    SubmissionDeadlineExceeded, // 6002

    #[msg("Submission deadline has not been reached yet.")]
    SubmissionDeadlineNotReached, // 6003

    #[msg("Admin review deadline has passed.")]
    AdminReviewDeadlineExceeded, // 6004

    #[msg("Technical evaluation deadline has passed.")]
    TechEvalDeadlineExceeded, // 6005

    #[msg("Financial reveal deadline has passed. Reveals are closed.")]
    FinancialRevealDeadlineExceeded, // 6006

    #[msg("Tender is not in SubmissionsOpen status.")]
    TenderNotSubmissionsOpen, // 6007

    #[msg("Tender is not in AdministrativeReview status.")]
    TenderNotAdminReview, // 6008

    #[msg("Tender is not in TechnicalEvaluation status.")]
    TenderNotTechnicalEvaluation, // 6009

    #[msg("Tender is not in FinancialEvaluation status.")]
    TenderNotFinancialEvaluation, // 6010

    #[msg("Tender has already been awarded.")]
    TenderAlreadyAwarded, // 6011

    #[msg("Bidder is not in the authorized whitelist.")]
    UnauthorizedBidder, // 6012

    #[msg("Merkle proof verification failed.")]
    InvalidMerkleProof, // 6013

    #[msg("Provided reveal preimage does not match the committed cryptographic hash.")]
    InvalidRevealHash, // 6014

    #[msg("Technical bid has already been revealed.")]
    TechAlreadyRevealed, // 6015

    #[msg("Technical proposal has not been revealed yet.")]
    TechNotRevealed, // 6016

    #[msg("Financial envelope has already been revealed.")]
    FinAlreadyRevealed, // 6017

    #[msg("Commercial Secrecy Invariant: Bidder is technically disqualified. Financial envelope is permanently sealed.")]
    BidderTechnicallyDisqualified, // 6018

    #[msg("Bidder has not passed administrative due diligence.")]
    BidderNotAdminPassed, // 6019

    #[msg("Winning bidder is not technically qualified.")]
    WinnerNotQualified, // 6020

    #[msg("Winning bidder has not unsealed their financial envelope.")]
    WinnerNotRevealed, // 6021

    #[msg("Selected winner does not have the lowest price in Least-Cost mode.")]
    WinnerNotLowestPrice, // 6022

    #[msg("Selected winner does not have the highest composite score in QCBS mode.")]
    WinnerNotHighestCompositeScore, // 6023

    #[msg("Anti-Lockout Gate: Financial reveal window is active and qualified bids remain unrevealed.")]
    FinancialRevealWindowActive, // 6024

    #[msg("Tender ID exceeds maximum allowed length of 32 characters.")]
    TenderIdTooLong, // 6025

    #[msg("Insufficient deposit attached for bid commitment bond.")]
    InsufficientDeposit, // 6026

    #[msg("Signer is not an accredited member of the Tender Committee.")]
    EvaluatorNotAuthorized, // 6027

    #[msg("Tender committee roster is already locked.")]
    CommitteeAlreadyLocked, // 6028

    #[msg("Evaluator grade has already been revealed.")]
    GradeAlreadyRevealed, // 6029

    #[msg("Evaluator grade has not been revealed yet.")]
    GradeNotRevealed, // 6030

    #[msg("At least 3 revealed committee evaluations required for trimmed mean scoring.")]
    InsufficientEvaluatorGrades, // 6031

    #[msg("Sub-scores do not match the claimed total score.")]
    InvalidSubScores, // 6032

    #[msg("Sub-scores exceed maximum allowed value (10,000 bps total).")]
    SubScoresOutOfRange, // 6033

    #[msg("Technical and financial weights must sum exactly to 10,000 basis points (100%).")]
    InvalidWeights, // 6034

    #[msg("Bond deposit has already been refunded or settled.")]
    BondAlreadySettled, // 6035

    #[msg("Bidder is technically qualified. Financial envelope must be unsealed to settle bond.")]
    BidderIsTechQualified, // 6036

    #[msg("Bond mode is not SolanaEscrow.")]
    InvalidBondMode, // 6037

    #[msg("Administrative review deadline has not been reached yet.")]
    AdminReviewDeadlineNotReached, // 6038

    #[msg("Technical evaluation deadline has not been reached yet.")]
    TechEvalDeadlineNotReached, // 6039

    #[msg("Revealed price cannot be zero.")]
    ZeroPriceNotAllowed, // 6040

    #[msg("All competing revealed bids must be provided for award validation.")]
    MissingCompetingBids, // 6041

    #[msg("Invalid competing bid account provided.")]
    InvalidCompetingBid, // 6042

    #[msg("Committee roster is incomplete: all accredited evaluator grades must be submitted.")]
    IncompleteCommitteeGrades, // 6043

    #[msg("Severe variance dropped all evaluator scores: empty trimmed score pool.")]
    EmptyTrimmedScorePool, // 6044

    #[msg("Bidder administrative compliance has already been evaluated.")]
    AdminAlreadyReviewed, // 6045

    #[msg("Technical score for this bid has already been finalized.")]
    TechnicalScoreAlreadyFinalized, // 6046
}
```

### 5.5 `programs/bidtrace/src/instructions/initialize_tender.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{EvaluationType, Tender, TenderMode, TenderStatus};

#[derive(Accounts)]
#[instruction(tender_id: String)]
pub struct InitializeTender<'info> {
    #[account(
        init,
        payer = authority,
        space = Tender::LEN,
        seeds = [b"tender", authority.key().as_ref(), tender_id.as_bytes()],
        bump
    )]
    pub tender: Account<'info, Tender>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handle_initialize_tender(
    ctx: Context<InitializeTender>,
    tender_id: String,
    ocds_notice_hash: [u8; 32],
    tender_mode: TenderMode,
    evaluation_type: EvaluationType,
    submission_deadline_slot: u64,
    admin_review_deadline_slot: u64,
    tech_eval_deadline_slot: u64,
    fin_reveal_deadline_slot: u64,
    authorized_bidders_root: [u8; 32],
    min_tech_score_bps: u16,
    tech_weight_bps: u16,
    fin_weight_bps: u16,
) -> Result<()> {
    require!(tender_id.len() <= 32, BidTraceError::TenderIdTooLong);

    let clock = Clock::get()?;
    require!(
        submission_deadline_slot > clock.slot,
        BidTraceError::InvalidSubmissionDeadline
    );
    require!(
        admin_review_deadline_slot >= submission_deadline_slot
            && tech_eval_deadline_slot >= admin_review_deadline_slot
            && fin_reveal_deadline_slot >= tech_eval_deadline_slot,
        BidTraceError::InvalidDeadlineSequence
    );

    if evaluation_type == EvaluationType::QCBS {
        require!(
            tech_weight_bps + fin_weight_bps == 10000,
            BidTraceError::InvalidWeights
        );
    }

    let tender = &mut ctx.accounts.tender;
    tender.authority = ctx.accounts.authority.key();
    tender.tender_id = tender_id;
    tender.ocds_notice_hash = ocds_notice_hash;
    tender.tender_mode = tender_mode;
    tender.evaluation_type = evaluation_type;
    tender.status = TenderStatus::SubmissionsOpen;

    tender.submission_deadline_slot = submission_deadline_slot;
    tender.admin_review_deadline_slot = admin_review_deadline_slot;
    tender.tech_eval_deadline_slot = tech_eval_deadline_slot;
    tender.fin_reveal_deadline_slot = fin_reveal_deadline_slot;

    tender.authorized_bidders_root = authorized_bidders_root;
    tender.min_tech_score_bps = min_tech_score_bps;
    tender.tech_weight_bps = tech_weight_bps;
    tender.fin_weight_bps = fin_weight_bps;

    tender.total_committed = 0;
    tender.total_admin_passed = 0;
    tender.total_tech_qualified = 0;
    tender.total_fin_revealed = 0;

    tender.lowest_revealed_price = u64::MAX;
    tender.highest_composite_score = 0;
    tender.winning_bidder = None;
    tender.bump = ctx.bumps.tender;

    Ok(())
}
```

### 5.6 `programs/bidtrace/src/instructions/initialize_committee.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{Tender, TenderCommittee};

#[derive(Accounts)]
pub struct InitializeCommittee<'info> {
    #[account(has_one = authority)]
    pub tender: Account<'info, Tender>,

    #[account(
        init,
        payer = authority,
        space = TenderCommittee::LEN,
        seeds = [b"committee", tender.key().as_ref()],
        bump
    )]
    pub committee: Account<'info, TenderCommittee>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handle_initialize_committee(
    ctx: Context<InitializeCommittee>,
    evaluators: Vec<Pubkey>,
    max_variance_bps: u16,
) -> Result<()> {
    require!(evaluators.len() >= 3, BidTraceError::InsufficientEvaluatorGrades);

    let committee = &mut ctx.accounts.committee;
    committee.tender = ctx.accounts.tender.key();
    committee.evaluators = evaluators;
    committee.max_variance_bps = max_variance_bps;
    committee.is_locked = true;
    committee.bump = ctx.bumps.committee;

    Ok(())
}
```

### 5.7 `programs/bidtrace/src/instructions/commit_dual_bid.rs`
```rust
use anchor_lang::prelude::*;
use anchor_lang::system_program;
use sha2::{Digest, Sha256};
use crate::errors::BidTraceError;
use crate::state::{AdminStatus, BondMode, DualBidCommitment, Tender, TenderMode, TenderStatus};

#[derive(Accounts)]
pub struct CommitDualBid<'info> {
    #[account(
        mut,
        constraint = tender.status == TenderStatus::SubmissionsOpen @ BidTraceError::TenderNotSubmissionsOpen,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        init,
        payer = fee_payer,
        space = DualBidCommitment::LEN,
        seeds = [b"bid", tender.key().as_ref(), bidder.key().as_ref()],
        bump
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub bidder: Signer<'info>,

    #[account(mut)]
    pub fee_payer: Signer<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handle_commit_dual_bid(
    ctx: Context<CommitDualBid>,
    admin_dossier_hash: [u8; 32],
    tech_commitment_hash: [u8; 32],
    fin_commitment_hash: [u8; 32],
    bond_mode: BondMode,
    bond_amount: u64,
    whitelist_proof: Option<Vec<[u8; 32]>>,
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;
    let bidder_key = ctx.accounts.bidder.key();

    // 1. Strict consensus slot submission deadline check
    require!(
        clock.slot <= tender.submission_deadline_slot,
        BidTraceError::SubmissionDeadlineExceeded
    );

    // 2. Model A: Pre-Qualified Merkle Whitelist Verification
    let mut admin_status = AdminStatus::Pending;
    if tender.tender_mode == TenderMode::PreQualifiedWhitelist {
        require!(
            tender.authorized_bidders_root != [0u8; 32],
            BidTraceError::UnauthorizedBidder
        );
        let proof = whitelist_proof.ok_or(BidTraceError::UnauthorizedBidder)?;

        require!(
            verify_whitelist_proof(&bidder_key, &proof, tender.authorized_bidders_root),
            BidTraceError::InvalidMerkleProof
        );

        admin_status = AdminStatus::Passed;
        tender.total_admin_passed += 1;
    } else if tender.admin_review_deadline_slot == tender.submission_deadline_slot {
        admin_status = AdminStatus::Passed;
        tender.total_admin_passed += 1;
    }

    // 3. Solana Escrow Bond Handling (if applicable)
    if bond_mode == BondMode::SolanaEscrow && bond_amount > 0 {
        system_program::transfer(
            CpiContext::new(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: ctx.accounts.fee_payer.to_account_info(),
                    to: ctx.accounts.bid_commitment.to_account_info(),
                },
            ),
            bond_amount,
        )?;
    }

    // 4. Record DualBidCommitment PDA
    let bid = &mut ctx.accounts.bid_commitment;
    bid.tender = tender.key();
    bid.bidder = bidder_key;
    bid.committed_at_slot = clock.slot;
    bid.admin_dossier_hash = admin_dossier_hash;
    bid.tech_commitment_hash = tech_commitment_hash;
    bid.fin_commitment_hash = fin_commitment_hash;
    bid.admin_status = admin_status;
    bid.admin_rejection_code = 0;

    bid.is_tech_revealed = false;
    bid.is_tech_finalized = false;
    bid.technical_score_bps = 0;
    bid.is_tech_qualified = false;

    bid.is_fin_revealed = false;
    bid.revealed_price = 0;
    bid.composite_score = 0;

    bid.bond_mode = bond_mode;
    bid.bond_amount = bond_amount;
    bid.is_bond_settled = false;
    bid.bump = ctx.bumps.bid_commitment;

    tender.total_committed += 1;

    Ok(())
}

/// Verifies a sorted-pair Merkle inclusion proof supporting both:
/// 1. Keccak-256 (OpenZeppelin / EVM standard)
/// 2. SHA-256 (Solana standard)
pub fn verify_whitelist_proof(
    bidder_key: &Pubkey,
    proof: &[[u8; 32]],
    expected_root: [u8; 32],
) -> bool {
    // 1. Keccak-256 path (OpenZeppelin / EVM standard)
    let mut current_keccak = anchor_lang::solana_program::keccak::hash(bidder_key.as_ref()).0;
    for sibling in proof {
        let (first, second) = if current_keccak <= *sibling {
            (&current_keccak, sibling)
        } else {
            (sibling, &current_keccak)
        };
        current_keccak = anchor_lang::solana_program::keccak::hashv(&[first, second]).0;
    }
    if current_keccak == expected_root {
        return true;
    }

    // 2. SHA-256 path (Solana standard)
    let mut leaf_hasher = Sha256::new();
    leaf_hasher.update(bidder_key.as_ref());
    let mut current_sha: [u8; 32] = leaf_hasher.finalize().into();

    for sibling in proof {
        let mut node_hasher = Sha256::new();
        if current_sha <= *sibling {
            node_hasher.update(&current_sha);
            node_hasher.update(sibling);
        } else {
            node_hasher.update(sibling);
            node_hasher.update(&current_sha);
        }
        current_sha = node_hasher.finalize().into();
    }
    current_sha == expected_root
}
```

### 5.8 `programs/bidtrace/src/instructions/advance_tender_phase.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{Tender, TenderStatus};

#[derive(Accounts)]
pub struct AdvanceTenderPhase<'info> {
    #[account(mut)]
    pub tender: Account<'info, Tender>,

    pub caller: Signer<'info>,
}

pub fn handle_advance_tender_phase(ctx: Context<AdvanceTenderPhase>) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;

    match tender.status {
        TenderStatus::SubmissionsOpen => {
            require!(
                clock.slot > tender.submission_deadline_slot,
                BidTraceError::SubmissionDeadlineNotReached
            );
            if tender.admin_review_deadline_slot == tender.submission_deadline_slot {
                tender.status = TenderStatus::TechnicalEvaluation;
            } else {
                tender.status = TenderStatus::AdministrativeReview;
            }
        }
        TenderStatus::AdministrativeReview => {
            require!(
                clock.slot > tender.admin_review_deadline_slot,
                BidTraceError::AdminReviewDeadlineNotReached
            );
            tender.status = TenderStatus::TechnicalEvaluation;
        }
        TenderStatus::TechnicalEvaluation => {
            require!(
                clock.slot > tender.tech_eval_deadline_slot,
                BidTraceError::TechEvalDeadlineNotReached
            );
            tender.status = TenderStatus::FinancialEvaluation;
        }
        _ => return Err(BidTraceError::TenderAlreadyAwarded.into()),
    }

    Ok(())
}
```

### 5.9 `programs/bidtrace/src/instructions/review_administrative_compliance.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{AdminStatus, DualBidCommitment, Tender, TenderStatus};

#[derive(Accounts)]
pub struct ReviewAdministrativeCompliance<'info> {
    #[account(
        mut,
        has_one = authority,
        constraint = tender.status == TenderStatus::AdministrativeReview @ BidTraceError::TenderNotAdminReview,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub authority: Signer<'info>,
}

pub fn handle_review_administrative_compliance(
    ctx: Context<ReviewAdministrativeCompliance>,
    passed: bool,
    rejection_code: u16,
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;
    let bid = &mut ctx.accounts.bid_commitment;

    require!(
        clock.slot <= tender.admin_review_deadline_slot,
        BidTraceError::AdminReviewDeadlineExceeded
    );
    require!(
        bid.admin_status == AdminStatus::Pending,
        BidTraceError::AdminAlreadyReviewed
    );

    if passed {
        bid.admin_status = AdminStatus::Passed;
        bid.admin_rejection_code = 0;
        tender.total_admin_passed = tender.total_admin_passed.checked_add(1).unwrap();
    } else {
        bid.admin_status = AdminStatus::Failed;
        bid.admin_rejection_code = rejection_code;
    }

    Ok(())
}
```

### 5.10 `programs/bidtrace/src/instructions/reveal_technical_bid.rs`
```rust
use anchor_lang::prelude::*;
use sha2::{Digest, Sha256};
use crate::errors::BidTraceError;
use crate::state::{AdminStatus, DualBidCommitment, Tender, TenderStatus};

#[derive(Accounts)]
pub struct RevealTechnicalBid<'info> {
    #[account(
        mut,
        constraint = tender.status == TenderStatus::TechnicalEvaluation @ BidTraceError::TenderNotTechnicalEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
        constraint = !bid_commitment.is_tech_revealed @ BidTraceError::TechAlreadyRevealed,
        constraint = bid_commitment.admin_status == AdminStatus::Passed @ BidTraceError::BidderNotAdminPassed,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub revealer: Signer<'info>,
}

pub fn handle_reveal_technical_bid(
    ctx: Context<RevealTechnicalBid>,
    salt_tech: [u8; 32],
    proposal_hash: [u8; 32],
) -> Result<()> {
    let tender = &ctx.accounts.tender;
    let bid = &mut ctx.accounts.bid_commitment;

    let mut hasher = Sha256::new();
    hasher.update(b"BIDTRACE_TECH_V1");
    hasher.update(tender.key().as_ref());
    hasher.update(bid.bidder.as_ref());
    hasher.update(&salt_tech);
    hasher.update(&proposal_hash);
    let computed_hash: [u8; 32] = hasher.finalize().into();

    require!(
        computed_hash == bid.tech_commitment_hash,
        BidTraceError::InvalidRevealHash
    );

    bid.is_tech_revealed = true;
    Ok(())
}
```

### 5.11 `programs/bidtrace/src/instructions/commit_evaluator_grade.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{DualBidCommitment, EvaluatorGrade, Tender, TenderCommittee, TenderStatus};

#[derive(Accounts)]
pub struct CommitEvaluatorGrade<'info> {
    #[account(
        constraint = tender.status == TenderStatus::TechnicalEvaluation @ BidTraceError::TenderNotTechnicalEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        seeds = [b"committee", tender.key().as_ref()],
        bump = committee.bump,
    )]
    pub committee: Account<'info, TenderCommittee>,

    #[account(
        seeds = [b"bid", tender.key().as_ref(), bidder.key().as_ref()],
        bump = bid_commitment.bump,
        constraint = bid_commitment.is_tech_revealed @ BidTraceError::TechNotRevealed,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    #[account(
        init,
        payer = evaluator,
        space = EvaluatorGrade::LEN,
        seeds = [b"grade", tender.key().as_ref(), evaluator.key().as_ref(), bidder.key().as_ref()],
        bump
    )]
    pub evaluator_grade: Account<'info, EvaluatorGrade>,

    #[account(mut)]
    pub evaluator: Signer<'info>,

    /// CHECK: Target bidder being scored
    pub bidder: AccountInfo<'info>,

    pub system_program: Program<'info, System>,
}

pub fn handle_commit_evaluator_grade(
    ctx: Context<CommitEvaluatorGrade>,
    commitment_hash: [u8; 32],
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &ctx.accounts.tender;
    let committee = &ctx.accounts.committee;
    let evaluator_key = ctx.accounts.evaluator.key();

    require!(
        committee.evaluators.contains(&evaluator_key),
        BidTraceError::EvaluatorNotAuthorized
    );
    require!(
        clock.slot <= tender.tech_eval_deadline_slot,
        BidTraceError::TechEvalDeadlineExceeded
    );

    let grade = &mut ctx.accounts.evaluator_grade;
    grade.tender = tender.key();
    grade.evaluator = evaluator_key;
    grade.bidder = ctx.accounts.bidder.key();
    grade.commitment_hash = commitment_hash;
    grade.committed_at_slot = clock.slot;
    grade.is_revealed = false;
    grade.sub_scores = [0; 5];
    grade.total_score_bps = 0;
    grade.justification_hash = [0; 32];
    grade.is_outlier_flagged = false;
    grade.bump = ctx.bumps.evaluator_grade;

    Ok(())
}
```

### 5.12 `programs/bidtrace/src/instructions/reveal_evaluator_grade.rs`
```rust
use anchor_lang::prelude::*;
use sha2::{Digest, Sha256};
use crate::errors::BidTraceError;
use crate::state::{EvaluatorGrade, Tender, TenderCommittee, TenderStatus};

#[derive(Accounts)]
pub struct RevealEvaluatorGrade<'info> {
    #[account(
        constraint = tender.status == TenderStatus::TechnicalEvaluation @ BidTraceError::TenderNotTechnicalEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        seeds = [b"committee", tender.key().as_ref()],
        bump = committee.bump,
    )]
    pub committee: Account<'info, TenderCommittee>,

    #[account(
        mut,
        seeds = [b"grade", tender.key().as_ref(), evaluator.key().as_ref(), bidder.key().as_ref()],
        bump = evaluator_grade.bump,
        constraint = !evaluator_grade.is_revealed @ BidTraceError::GradeAlreadyRevealed,
    )]
    pub evaluator_grade: Account<'info, EvaluatorGrade>,

    pub evaluator: Signer<'info>,

    /// CHECK: Target bidder being scored
    pub bidder: AccountInfo<'info>,
}

pub fn handle_reveal_evaluator_grade(
    ctx: Context<RevealEvaluatorGrade>,
    sub_scores: [u16; 5],
    salt: [u8; 32],
    justification_hash: [u8; 32],
) -> Result<()> {
    let tender = &ctx.accounts.tender;
    let evaluator_key = ctx.accounts.evaluator.key();
    let bidder_key = ctx.accounts.bidder.key();
    let grade = &mut ctx.accounts.evaluator_grade;

    let total_sum: u32 = sub_scores.iter().map(|&s| s as u32).sum();
    require!(total_sum <= 10000, BidTraceError::SubScoresOutOfRange);

    let mut hasher = Sha256::new();
    hasher.update(b"BIDTRACE_GRADE_V1");
    hasher.update(tender.key().as_ref());
    hasher.update(bidder_key.as_ref());
    hasher.update(evaluator_key.as_ref());
    hasher.update(&salt);
    for score in sub_scores.iter() {
        hasher.update(&score.to_le_bytes());
    }
    hasher.update(&justification_hash);
    let computed_hash: [u8; 32] = hasher.finalize().into();

    require!(
        computed_hash == grade.commitment_hash,
        BidTraceError::InvalidRevealHash
    );

    grade.is_revealed = true;
    grade.sub_scores = sub_scores;
    grade.total_score_bps = total_sum as u16;
    grade.justification_hash = justification_hash;

    Ok(())
}
```

### 5.13 `programs/bidtrace/src/instructions/finalize_technical_scores.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{DualBidCommitment, EvaluatorGrade, Tender, TenderCommittee, TenderStatus};

#[derive(Accounts)]
pub struct FinalizeTechnicalScores<'info> {
    #[account(
        mut,
        has_one = authority,
        constraint = tender.status == TenderStatus::TechnicalEvaluation @ BidTraceError::TenderNotTechnicalEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        seeds = [b"committee", tender.key().as_ref()],
        bump = committee.bump,
    )]
    pub committee: Account<'info, TenderCommittee>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
        constraint = bid_commitment.is_tech_revealed @ BidTraceError::TechNotRevealed,
        constraint = !bid_commitment.is_tech_finalized @ BidTraceError::TechnicalScoreAlreadyFinalized,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub authority: Signer<'info>,
}

pub fn handle_finalize_technical_scores<'info>(
    ctx: Context<'_, '_, '_, 'info, FinalizeTechnicalScores<'info>>,
) -> Result<()> {
    let tender = &mut ctx.accounts.tender;
    let committee = &ctx.accounts.committee;
    let bid_commitment = &mut ctx.accounts.bid_commitment;

    let remaining = ctx.remaining_accounts;
    require!(remaining.len() >= 3, BidTraceError::InsufficientEvaluatorGrades);
    require!(
        remaining.len() == committee.evaluators.len(),
        BidTraceError::IncompleteCommitteeGrades
    );

    struct GradeEntry {
        acc_index: usize,
        _evaluator: Pubkey,
        total_score_bps: u16,
    }

    let mut entries: Vec<GradeEntry> = Vec::with_capacity(remaining.len());
    let mut seen_evaluators: Vec<Pubkey> = Vec::with_capacity(remaining.len());

    for (idx, acc) in remaining.iter().enumerate() {
        require!(acc.owner == &crate::ID, BidTraceError::EvaluatorNotAuthorized);

        let data = acc.try_borrow_data()?;
        let grade = EvaluatorGrade::try_deserialize(&mut &data[..])?;

        require!(grade.tender == tender.key(), BidTraceError::EvaluatorNotAuthorized);
        require!(grade.bidder == bid_commitment.bidder, BidTraceError::EvaluatorNotAuthorized);
        require!(grade.is_revealed, BidTraceError::GradeNotRevealed);
        require!(committee.evaluators.contains(&grade.evaluator), BidTraceError::EvaluatorNotAuthorized);
        require!(!seen_evaluators.contains(&grade.evaluator), BidTraceError::EvaluatorNotAuthorized);

        seen_evaluators.push(grade.evaluator);
        entries.push(GradeEntry {
            acc_index: idx,
            _evaluator: grade.evaluator,
            total_score_bps: grade.total_score_bps,
        });
    }

    let n = entries.len();
    let mut scores: Vec<u32> = entries.iter().map(|e| e.total_score_bps as u32).collect();
    scores.sort();

    let median: u32 = if n % 2 == 1 {
        scores[n / 2]
    } else {
        (scores[n / 2 - 1] + scores[n / 2]) / 2
    };

    let raw_delta = (median * committee.max_variance_bps as u32) / 10000;
    let max_allowed_delta = raw_delta.max(100);

    for entry in entries.iter() {
        let score = entry.total_score_bps as u32;
        let delta = if score >= median { score - median } else { median - score };
        let is_outlier = delta > max_allowed_delta;

        let acc = &remaining[entry.acc_index];
        let mut data = acc.try_borrow_mut_data()?;
        let mut grade = EvaluatorGrade::try_deserialize(&mut &data[..])?;
        grade.is_outlier_flagged = is_outlier;
        grade.try_serialize(&mut &mut data[..])?;
    }

    let final_score: u32 = if n >= 4 {
        let mut accepted: Vec<u32> = Vec::new();
        for &s in scores[1..n - 1].iter() {
            let delta = if s >= median { s - median } else { median - s };
            if delta <= max_allowed_delta {
                accepted.push(s);
            }
        }
        require!(!accepted.is_empty(), BidTraceError::EmptyTrimmedScorePool);
        let sum: u32 = accepted.iter().sum();
        sum / accepted.len() as u32
    } else {
        let mut accepted: Vec<u32> = Vec::new();
        for &s in scores.iter() {
            let delta = if s >= median { s - median } else { median - s };
            if delta <= max_allowed_delta {
                accepted.push(s);
            }
        }
        require!(!accepted.is_empty(), BidTraceError::EmptyTrimmedScorePool);
        let sum: u32 = accepted.iter().sum();
        sum / accepted.len() as u32
    };

    let final_score_bps = final_score as u16;
    let is_qualified = final_score_bps >= tender.min_tech_score_bps;

    bid_commitment.technical_score_bps = final_score_bps;
    bid_commitment.is_tech_qualified = is_qualified;
    bid_commitment.is_tech_finalized = true;

    if is_qualified {
        tender.total_tech_qualified = tender.total_tech_qualified.checked_add(1).unwrap();
    }

    Ok(())
}
```

### 5.14 `programs/bidtrace/src/instructions/reveal_financial_envelope.rs`
```rust
use anchor_lang::prelude::*;
use sha2::{Digest, Sha256};
use crate::errors::BidTraceError;
use crate::state::{BondMode, DualBidCommitment, Tender, TenderStatus};

#[derive(Accounts)]
pub struct RevealFinancialEnvelope<'info> {
    #[account(
        mut,
        constraint = tender.status == TenderStatus::FinancialEvaluation @ BidTraceError::TenderNotFinancialEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
        constraint = !bid_commitment.is_fin_revealed @ BidTraceError::FinAlreadyRevealed,
        // COMMERCIAL SECRECY GUARANTEE: Permanently seals disqualified financial envelopes
        constraint = bid_commitment.is_tech_qualified @ BidTraceError::BidderTechnicallyDisqualified,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub revealer: Signer<'info>,

    #[account(
        mut,
        constraint = bidder_recipient.key() == bid_commitment.bidder
    )]
    pub bidder_recipient: AccountInfo<'info>,
}

pub fn handle_reveal_financial_envelope(
    ctx: Context<RevealFinancialEnvelope>,
    salt_fin: [u8; 32],
    price: u64,
    boq_hash: [u8; 32],
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;
    let bid = &mut ctx.accounts.bid_commitment;

    require!(
        clock.slot <= tender.fin_reveal_deadline_slot,
        BidTraceError::FinancialRevealDeadlineExceeded
    );
    require!(price > 0, BidTraceError::ZeroPriceNotAllowed);

    let mut hasher = Sha256::new();
    hasher.update(b"BIDTRACE_FIN_V1");
    hasher.update(tender.key().as_ref());
    hasher.update(bid.bidder.as_ref());
    hasher.update(&salt_fin);
    hasher.update(&price.to_le_bytes());
    hasher.update(&boq_hash);
    let computed_hash: [u8; 32] = hasher.finalize().into();

    require!(
        computed_hash == bid.fin_commitment_hash,
        BidTraceError::InvalidRevealHash
    );

    bid.is_fin_revealed = true;
    bid.revealed_price = price;
    tender.total_fin_revealed += 1;

    if price < tender.lowest_revealed_price {
        tender.lowest_revealed_price = price;
    }

    if bid.bond_mode == BondMode::SolanaEscrow && bid.bond_amount > 0 && !bid.is_bond_settled {
        let refund_lamports = bid.bond_amount;
        bid.is_bond_settled = true;
        **bid.to_account_info().try_borrow_mut_lamports()? -= refund_lamports;
        **ctx.accounts.bidder_recipient.try_borrow_mut_lamports()? += refund_lamports;
    }

    Ok(())
}
```

### 5.15 `programs/bidtrace/src/instructions/record_award_qcbs.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{DualBidCommitment, EvaluationType, Tender, TenderStatus};

#[derive(Accounts)]
pub struct RecordAwardQcbs<'info> {
    #[account(
        mut,
        has_one = authority,
        constraint = tender.status == TenderStatus::FinancialEvaluation @ BidTraceError::TenderNotFinancialEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), winning_bid.bidder.as_ref()],
        bump = winning_bid.bump,
        constraint = winning_bid.is_tech_qualified @ BidTraceError::WinnerNotQualified,
        constraint = winning_bid.is_fin_revealed @ BidTraceError::WinnerNotRevealed,
    )]
    pub winning_bid: Account<'info, DualBidCommitment>,

    pub authority: Signer<'info>,
}

pub fn handle_record_award_qcbs<'info>(
    ctx: Context<'_, '_, '_, 'info, RecordAwardQcbs<'info>>,
    _rationale_hash: [u8; 32],
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;
    let winning_bid = &mut ctx.accounts.winning_bid;

    // 1. Anti-Lockout Gate:
    require!(
        clock.slot > tender.fin_reveal_deadline_slot
            || tender.total_fin_revealed == tender.total_tech_qualified,
        BidTraceError::FinancialRevealWindowActive
    );

    // 2. Zero-Price Guards (SEC-04)
    require!(winning_bid.revealed_price > 0, BidTraceError::ZeroPriceNotAllowed);
    require!(
        tender.lowest_revealed_price > 0 && tender.lowest_revealed_price <= winning_bid.revealed_price,
        BidTraceError::ZeroPriceNotAllowed
    );

    // 3. Programmatic QCBS Composite Score Calculation
    let winning_composite_score: u64 = match tender.evaluation_type {
        EvaluationType::LeastCost => {
            require!(
                winning_bid.revealed_price == tender.lowest_revealed_price,
                BidTraceError::WinnerNotLowestPrice
            );
            10000
        }
        EvaluationType::QCBS => {
            let tech_part = (winning_bid.technical_score_bps as u128
                * tender.tech_weight_bps as u128) / 10000;
            let fin_score_ratio = (tender.lowest_revealed_price as u128 * 10000)
                / winning_bid.revealed_price as u128;
            let fin_part = (fin_score_ratio * tender.fin_weight_bps as u128) / 10000;
            (tech_part + fin_part) as u64
        }
    };

    // 4. Mathematical Comparison Against All Competing Revealed Qualified Bids (SEC-04)
    let expected_competing_count = tender.total_fin_revealed.saturating_sub(1) as usize;
    require!(
        ctx.remaining_accounts.len() == expected_competing_count,
        BidTraceError::MissingCompetingBids
    );

    let mut seen_competing_bidders: Vec<Pubkey> = Vec::with_capacity(expected_competing_count);

    for acc in ctx.remaining_accounts.iter() {
        require!(acc.owner == ctx.program_id, BidTraceError::InvalidCompetingBid);

        let competing_bid = {
            let data = acc.try_borrow_data()?;
            DualBidCommitment::try_deserialize(&mut &data[..])?
        };

        require!(competing_bid.tender == tender.key(), BidTraceError::InvalidCompetingBid);

        let (expected_pda, expected_bump) = Pubkey::find_program_address(
            &[b"bid", tender.key().as_ref(), competing_bid.bidder.as_ref()],
            ctx.program_id,
        );
        require!(
            acc.key() == expected_pda && competing_bid.bump == expected_bump,
            BidTraceError::InvalidCompetingBid
        );
        require!(competing_bid.bidder != winning_bid.bidder, BidTraceError::InvalidCompetingBid);
        require!(!seen_competing_bidders.contains(&competing_bid.bidder), BidTraceError::InvalidCompetingBid);
        seen_competing_bidders.push(competing_bid.bidder);

        require!(competing_bid.is_tech_qualified && competing_bid.is_fin_revealed, BidTraceError::InvalidCompetingBid);
        require!(competing_bid.revealed_price > 0, BidTraceError::ZeroPriceNotAllowed);

        let competing_composite_score: u64 = match tender.evaluation_type {
            EvaluationType::LeastCost => {
                require!(winning_bid.revealed_price <= competing_bid.revealed_price, BidTraceError::WinnerNotLowestPrice);
                if competing_bid.revealed_price == tender.lowest_revealed_price { 10000 } else { 0 }
            }
            EvaluationType::QCBS => {
                let tech_part = (competing_bid.technical_score_bps as u128 * tender.tech_weight_bps as u128) / 10000;
                let fin_score_ratio = (tender.lowest_revealed_price as u128 * 10000) / competing_bid.revealed_price as u128;
                let fin_part = (fin_score_ratio * tender.fin_weight_bps as u128) / 10000;
                let comp_total = (tech_part + fin_part) as u64;

                // Authority cannot award an inferior-scoring bidder
                require!(winning_composite_score >= comp_total, BidTraceError::WinnerNotHighestCompositeScore);
                comp_total
            }
        };

        if acc.is_writable {
            let mut mut_data = acc.try_borrow_mut_data()?;
            let mut mutable_bid = DualBidCommitment::try_deserialize(&mut &mut_data[..])?;
            mutable_bid.composite_score = competing_composite_score;
            mutable_bid.try_serialize(&mut &mut mut_data[..])?;
        }
    }

    winning_bid.composite_score = winning_composite_score;
    tender.highest_composite_score = winning_composite_score;
    tender.winning_bidder = Some(winning_bid.bidder);
    tender.status = TenderStatus::Awarded;

    Ok(())
}
```

### 5.16 `programs/bidtrace/src/instructions/refund_disqualified_bond.rs`
```rust
use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{BondMode, DualBidCommitment, Tender, TenderStatus};

#[derive(Accounts)]
pub struct RefundDisqualifiedBond<'info> {
    #[account(
        constraint = tender.status >= TenderStatus::FinancialEvaluation @ BidTraceError::TenderNotFinancialEvaluation,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
        // Commercial Secrecy Protection: ONLY technically disqualified bidders use this instruction!
        constraint = !bid_commitment.is_tech_qualified @ BidTraceError::BidderIsTechQualified,
        constraint = !bid_commitment.is_bond_settled @ BidTraceError::BondAlreadySettled,
        constraint = bid_commitment.bond_mode == BondMode::SolanaEscrow @ BidTraceError::InvalidBondMode,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    #[account(
        mut,
        constraint = bidder_recipient.key() == bid_commitment.bidder
    )]
    pub bidder_recipient: AccountInfo<'info>,

    pub caller: Signer<'info>,
}

pub fn handle_refund_disqualified_bond(ctx: Context<RefundDisqualifiedBond>) -> Result<()> {
    let bid = &mut ctx.accounts.bid_commitment;
    let refund_amount = bid.bond_amount;

    require!(refund_amount > 0, BidTraceError::InsufficientDeposit);
    bid.is_bond_settled = true;

    **bid.to_account_info().try_borrow_mut_lamports()? -= refund_amount;
    **ctx.accounts.bidder_recipient.try_borrow_mut_lamports()? += refund_amount;

    Ok(())
}
```

---

## 6. Off-Chain Reference Engine & REST Gateway

### 6.1 `bidtrace_py/merkle.py` (Dual Keccak-256 / SHA-256 Engine)
```python
import hashlib
from typing import List, Dict, Any, Optional, Union
from .crypto import to_32bytes

def keccak_256(data: bytes) -> bytes:
    """
    Pure Python zero-dependency Keccak-256 implementation (FIPS 202 Keccak-f[1600] permutation).
    Matches Ethereum keccak256, OpenZeppelin MerkleProof, and solana_program::keccak::hash syscall.
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
    padded = data + (bytes([0x81]) if padlen == 1 else bytes([0x01]) + bytes(padlen - 2) + bytes([0x80]))

    for block_idx in range(0, len(padded), rate):
        block = padded[block_idx:block_idx + rate]
        for i in range(rate // 8):
            state[i % 5][i // 5] ^= int.from_bytes(block[i * 8:(i + 1) * 8], "little")

        for round_idx in range(24):
            C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
            D = [C[(x - 1) % 5] ^ rol64(C[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    state[x][y] ^= D[x]

            B = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2 * x + 3 * y) % 5] = rol64(state[x][y], ROTC[x][y])

            for x in range(5):
                for y in range(5):
                    state[x][y] = (B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])) & 0xFFFFFFFFFFFFFFFF

            state[0][0] ^= RC[round_idx]

    out = bytearray()
    for i in range(4):
        out += state[i % 5][i // 5].to_bytes(8, "little")
    return bytes(out)

def compute_leaf(bidder_key: Any, algorithm: str = "sha256") -> bytes:
    raw_key = to_32bytes(bidder_key)
    if algorithm.lower() in ("keccak", "keccak256", "keccak-256"):
        return keccak_256(raw_key)
    return hashlib.sha256(raw_key).digest()

def hash_pair(a: bytes, b: bytes, algorithm: str = "sha256") -> bytes:
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
    root_bytes = to_32bytes(root)
    algorithms = [algorithm] if algorithm else ["sha256", "keccak256"]
    for algo in algorithms:
        current = compute_leaf(bidder_key, algorithm=algo)
        for sib in proof:
            current = hash_pair(current, to_32bytes(sib), algorithm=algo)
        if current == root_bytes:
            return True
    return False

class MerkleTree:
    def __init__(self, bidders: List[Any], algorithm: str = "sha256"):
        self.algorithm = algorithm.lower()
        self.raw_bidders = list(bidders)
        self.leaves = [compute_leaf(b, algorithm=self.algorithm) for b in self.raw_bidders]
        self.levels = [self.leaves]
        self._build_tree()

    def _build_tree(self):
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
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
        target = compute_leaf(bidder_key, algorithm=self.algorithm)
        idx = self.leaves.index(target)
        proof = []
        for level in self.levels[:-1]:
            sib_idx = idx - 1 if idx % 2 == 1 else idx + 1
            proof.append(level[sib_idx] if sib_idx < len(level) else level[idx])
            idx //= 2
        return proof

    def get_proof_hex(self, bidder_key: Any) -> List[str]:
        return [p.hex() for p in self.get_proof(bidder_key)]
```

---

## 7. Comprehensive Test Suites & Verification Proofs

### 7.1 Anchor Localnet Integration Tests (`tests/bidtrace.ts`)
Run command: `anchor test --skip-build` in WSL / Linux.
**Result: 14 / 14 Passing (100% Passing)**

```
  BidTrace 3.0: Incorruptible Two-Envelope & Blinded Scoring Protocol
    ✔ Test 1: Authority initializes Two-Envelope QCBS Tender with OCDS Hash and Deadlines (423ms)
    ✔ Test 2: Authority initializes Tender Committee with 5 accredited evaluators (432ms)
    ✔ Test 3: Contractors submit confidential Dual-Envelope Bids (A & B) (868ms)
    ✔ Test 4: Tender advances to Technical Evaluation and unseals Envelope A (2552ms)
    ✔ Test 5: Evaluators submit and unseal blinded grades (including adversarial outlier) (8599ms)
    ✔ Test 6: On-chain Olympic Trimmed Mean flags Rogue Evaluator & Qualifies Bidder A while Disqualifying Bidder B (893ms)
    ✔ Test 7 (Commercial Secrecy Invariant): Disqualified Bidder B is strictly prevented from unsealing Financial Envelope (6915ms)
    ✔ Test 7b (SEC-01 Fix): Disqualified Bidder B reclaims escrowed bond without leaking Envelope B (424ms)
    ✔ Test 8: Qualified Bidder A unseals Financial Envelope and wins QCBS Award (837ms)
    ✔ Test 8b (SEC-04 Fix): Anti-Arbitrary Winner Verification & Zero-Price Guard in QCBS Mode (13169ms)
    ✔ Test 8c (SEC-05 Fix): Committee Inclusivity, Zero-Median Variance Floor & Empty Trimmed Pool Revert (12314ms)
    ✔ Test 8d (SEC-06 Fix): Administrative Due Diligence in Model B & Technical Reveal Gating (10076ms)
    ✔ Test 8e (SEC-07 Target 2 Fix): Post-Award State Machine Lockout - TenderNotTechnicalEvaluation
    ✔ Test 8f (SEC-08 Target 3 Fix): Model A Pre-Qualified Merkle Whitelist Verification with Keccak-256 and SHA-256 (2983ms)

  14 passing (1m)
```

### 7.2 Python Test Suites (`python -m unittest discover tests`)
Run command: `python -m unittest discover -s tests -p "test_*.py"`
**Result: 78 / 78 Passing (100% Passing)**

- `tests/test_sec07_double_finalization_guard.py` (`8 / 8 Passing`): Validates double finalization protection on qualified and disqualified bidders, authority checks, status constraints, REST 400 rejection, and total_tech_qualified counter stability.
- `tests/test_sec08_merkle_hashing_parity.py` (`8 / 8 Passing`): Validates NIST/Ethereum Keccak-256 vectors, commutative sorted pairs, tree generation, cross-algorithm isolation, and Model A commitments under both Keccak-256 and SHA-256.
- `tests/test_engine.py`, `tests/test_phase3_relayer.py`, `tests/test_phase4_verifier.py`, `tests/test_exploit.py` (`62 / 62 Passing`): Full end-to-end integration, REST API, OCDS JCS hashing, and air-gapped verifier testing.

### 7.3 Cross-Language RFC 8785 Hash Parity Proof
Byte-for-byte identical across Python 3.13 and Node.js v20:
`64b57de746bea5a2d9fea955ed5ebb56ad32cf217e44c1c4dc247d855884b376`

---

## 8. Adversarial Attack Defense Matrix

| Target ID | Vulnerability / Attack Vector | Attacker Action | Smart Contract Defense & Line Anchor | Test Proof |
| :---: | :--- | :--- | :--- | :--- |
| **SEC-01** | Disqualified Bond Lockup | Disqualified bidder tries to reclaim bond but contract requires unsealing Envelope B. | `refund_disqualified_bond.rs`: allows escrow refund if `!is_tech_qualified` without calling reveal. | `bidtrace.ts` Test 7b |
| **SEC-02** | Insider Data Leak | Relayer leaks unsealed financial quotations early. | Preimages stored strictly off-server; financial keys unsealed only via on-chain verified events. | `test_engine.py` |
| **SEC-03** | Authority Early Lockout | Buyer calls `advance_tender_phase` early to freeze out honest contractors. | `advance_tender_phase.rs`: `require!(clock.slot > deadline, SubmissionDeadlineNotReached)`. | `bidtrace.ts` Test 4 |
| **SEC-04** | Arbitrary Winner Selection | Authority picks higher-priced or lower-scoring contractor. | `record_award_qcbs.rs`: mathematically compares all competing bids in `remaining_accounts`. | `bidtrace.ts` Test 8b |
| **SEC-05** | Rogue Evaluator Favoritism | Corrupt evaluator submits 98% to inflate favored friend. | `finalize_technical_scores.rs`: Olympic Trimmed Mean drops max/min; sets `is_outlier_flagged`. | `bidtrace.ts` Test 6 |
| **SEC-06** | Administrative Due Diligence Gating | Contractor unseals technical bid before passing compliance review. | `reveal_technical_bid.rs`: `constraint = bid.admin_status == AdminStatus::Passed`. | `bidtrace.ts` Test 8d |
| **SEC-07** | Double Finalization Drift | Authority re-finalizes bidder to inflate `total_tech_qualified` and game anti-lockout gate. | `finalize_technical_scores.rs`: `constraint = !bid.is_tech_finalized`, sets `is_tech_finalized = true`. | `test_sec07_double_finalization_guard.py` |
| **SEC-08** | Merkle Whitelist Fraud | Unvetted bidder submits forged proof or uses EVM Keccak proof against SHA contract. | `commit_dual_bid.rs`: dual-hash engine validates Keccak-256 and SHA-256; throws `InvalidMerkleProof`. | `test_sec08_merkle_hashing_parity.py`, `bidtrace.ts` Test 8f |
| **SEC-09** | Division-by-Zero / Zero Price | Bidder submits $0 price to trigger math panic in QCBS formula. | `reveal_financial_envelope.rs`: `require!(price > 0, ZeroPriceNotAllowed)`. | `bidtrace.ts` Test 8b |
| **SEC-10** | Commercial Secrecy Breach | Buyer/competitor attempts to unseal disqualified bidder's Envelope B. | `reveal_financial_envelope.rs`: `constraint = bid.is_tech_qualified`. | `bidtrace.ts` Test 7 |

---

## 9. Colosseum Hackathon & Venture Evaluation Rubric Alignment

| Colosseum Hackathon Criterion | BidTrace Realization & Engineering Depth |
| :--- | :--- |
| **1. Novelty & Technical Ambition** | First protocol uniting **OCDS 1.1**, **RFC 8785 JCS**, **Solana consensus slots**, and **Two-Envelope Commercial Secrecy**. Implements the world's first on-chain Olympic Trimmed Mean scoring engine with median-based outlier pruning. |
| **2. Architecture on Solana** | Unlocks capabilities impossible on Ethereum or L2s: **400ms slot finality** prevents deadline race conditions; **Sealevel parallel execution** across independent `DualBidCommitment` PDAs; **sub-cent transaction fees** make micro-commitments viable. |
| **3. Real-World Feasibility & GTM** | **Fiat-to-Gas Decoupling**: Enterprise buyers and contractors interact via fiat invoicing and standard SSO. The relayer pays gas and handles Solana transactions seamlessly. |
| **4. Multi-Jurisdiction Legal Compliance** | Directly supports World Bank Debarment Covenants (BSD), FIDIC engineering contracts, TradFi Surety policies, and MT760 SWIFT bank guarantees. |
| **5. Engineering Rigor & Completeness** | 100% complete production stack: 12 Anchor Rust instructions, 78 Python tests passing, 14 Anchor localnet tests passing, REST API Gateway running, standalone Air-Gapped CLI verifier, and multi-portal web dashboard. |

---

## 10. Unit Economics & GTM Strategy

- **Total Addressable Market (TAM):** $13 Trillion Global Public Procurement.
- **Serviceable Addressable Market (SAM):** $90 Billion in annual Multilateral Development Bank (World Bank, ADB, EBRD, AfDB) sovereign infrastructure loans subject to strict anti-corruption audit mandates.
- **SaaS Pricing Model:** 0.05% of tender value capped at $25,000 per international tender (vs traditional procurement audit fees of $250,000+).
- **On-Chain Solana Costs:** $\approx 0.015\text{ SOL}$ per complete 5-bidder tender lifecycle ($\approx \$2.25\text{ USD}$), yielding **$>99.9\%$ gross profit margins** for the BidTrace relayer.
- **Defensibility:** Network effects driven by immutable on-chain track records of evaluator objectivity and contractor bid commitments.
