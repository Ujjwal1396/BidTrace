/**
 * BidTrace Central Frontend Config (Phase 1-3 redesign)
 * Single source of truth — replaces hardcoded values scattered across index.html.
 */
window.BidTraceConfig = {
  programId: "x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ",
  explorerBase: "https://explorer.solana.com/address",
  rpcUrl: "https://api.devnet.solana.com",
  slots: { base: 1000, deadline: 1050, lock: 1060, eval: 1080, award: 1110 },
  defaults: {
    tenderId: "TENDER-QCBS-2026-001",
    buyerName: "Ministry of Transportation & Infrastructure",
    title: "National Highway 402 Corridor Modernization & Bridge Expansion",
    estimatedAmount: 3800000,
    bondAmount: 190000,
    techWeight: 0.70,
    finWeight: 0.30,
    minScore: 75.0
  },
  presets: [
    { name: "ACME Infrastructure Corp", price: 3800000, bondMode: 1, note: "Qualifies & wins QCBS", rank: "Rank 1" },
    { name: "Apex Civil Engineering", price: 4100000, bondMode: 2, note: "Qualifies at ~83%", rank: "Rank 2" },
    { name: "Rogue Non-Compliant Builder", price: 2900000, bondMode: 3, note: "Fails tech, stays sealed", rank: "Sealed" }
  ],
  templates: [
    { id: "highway-qcbs", label: "Highway QCBS 70/30", techWeight: 0.70, finWeight: 0.30, minScore: 75.0, bond: 190000 },
    { id: "worldbank-open", label: "World Bank Open (Least Cost)", techWeight: 0.60, finWeight: 0.40, minScore: 70.0, bond: 150000 },
    { id: "epc-selective", label: "Private EPC Selective", techWeight: 0.80, finWeight: 0.20, minScore: 80.0, bond: 250000 }
  ],
  bondModes: {
    0: { label: "Solana Escrow", hint: "Native lamports locked in non-custodial PDA." },
    1: { label: "Surety MGA ($250 Fiat)", hint: "TradFi Surety-as-a-Service: GIA JCS hash attached." },
    2: { label: "MT760 Bank Guarantee", hint: "SWIFT BIC + URDG 758 attestation hash." },
    3: { label: "World Bank BSD", hint: "3-year debarment covenant. No collateral." }
  },
  storageKeys: { receipts: "bidtrace_receipts_v1", mode: "bidtrace_ui_mode", tender: "bidtrace_last_tender" }
};
