import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_BG = RGBColor(10, 15, 29)          # Deep Midnight
    C_CARD = RGBColor(18, 25, 45)        # Card Background
    C_CARD_BORDER = RGBColor(30, 41, 70) # Subtle Card Border
    C_WHITE = RGBColor(255, 255, 255)
    C_CYAN = RGBColor(6, 182, 212)       # Electric Cyan
    C_PURPLE = RGBColor(168, 85, 247)    # Purple
    C_TEXT_MUTED = RGBColor(148, 163, 184) # Muted Grey
    C_ROSE = RGBColor(244, 63, 94)       # Danger Rose
    C_EMERALD = RGBColor(16, 185, 129)   # Emerald
    C_AMBER = RGBColor(245, 158, 11)     # Amber

    logo_path = os.path.abspath("public/logo-mark.png")

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_card(slide, left, top, width, height, bg_color=C_CARD, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: COVER (MINIMALIST & BOLD)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Logo Emblem
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(1.2), Inches(1.6), width=Inches(1.8))

    # Hackathon Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), Inches(1.65), Inches(3.8), Inches(0.45))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(16, 32, 55)
    b1.line.color.rgb = C_CYAN
    b1.text_frame.text = "COLOSSEUM CRYPTO WORLD'S FAIR 2026"
    b1.text_frame.paragraphs[0].font.size = Pt(11)
    b1.text_frame.paragraphs[0].font.bold = True
    b1.text_frame.paragraphs[0].font.color.rgb = C_CYAN
    b1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Brand Title
    tb_title = s1.shapes.add_textbox(Inches(3.2), Inches(2.15), Inches(9.0), Inches(1.2))
    p = tb_title.text_frame.paragraphs[0]
    p.text = "BidTrace"
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Big Winning Headline
    tb_h = s1.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(11.0), Inches(1.3))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "Tamper-Proof Sealed Bidding for Public Contracts on Solana"
    p_h.font.size = Pt(32)
    p_h.font.bold = True
    p_h.font.color.rgb = C_CYAN

    # 3 Stat Cards (Big Numbers, Minimal Text)
    stats_s1 = [
        ("$13.0 Trillion", "Protected Market", C_CYAN),
        ("400ms Clock", "Proof of History", C_PURPLE),
        ("Zero Crypto Gas", "Enterprise Sponsored", C_EMERALD)
    ]
    for i, (num, lbl, col) in enumerate(stats_s1):
        bx = Inches(1.2 + i * 3.75)
        add_card(s1, bx, Inches(5.3), Inches(3.5), Inches(1.4))
        tb_st = s1.shapes.add_textbox(bx + Inches(0.2), Inches(5.4), Inches(3.1), Inches(1.2))
        tf_st = tb_st.text_frame
        p_n = tf_st.paragraphs[0]
        p_n.text = num
        p_n.font.size = Pt(26)
        p_n.font.bold = True
        p_n.font.color.rgb = col
        p_l = tf_st.add_paragraph()
        p_l.text = lbl
        p_l.font.size = Pt(13)
        p_l.font.color.rgb = C_TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "[SLIDE 1 | 0:00 - 0:15 | 32 Words]\n"
        "\"Judges, every year, $13 trillion is spent on public infrastructure. "
        "Yet the entire industry relies on centralized database trust. "
        "BidTrace brings tamper-proof sealed bidding to public contracts on Solana, "
        "making corruption mathematically impossible.\""
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM (COMPARISON CARDS, ZERO FLUFF)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)

    th2 = s2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf2 = th2.text_frame
    p = tf2.paragraphs[0]
    p.text = "THE $13 TRILLION VULNERABILITY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p2 = tf2.add_paragraph()
    p2.text = "The Post-Deadline Insider Tampering Window"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # Left Card: Traditional Centralized Failures (Punchy Bullets)
    add_card(s2, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.8), bg_color=C_CARD, border_color=RGBColor(80, 20, 35))
    tfl = s2.shapes.add_textbox(Inches(1.3), Inches(2.1), Inches(4.8), Inches(4.4)).text_frame
    tfl.word_wrap = True
    pl = tfl.paragraphs[0]
    pl.text = "✖  Centralized E-Procurement"
    pl.font.size = Pt(20)
    pl.font.bold = True
    pl.font.color.rgb = C_ROSE

    items_bad = [
        "Root Admin God-Mode (Unencrypted bid peek)",
        "Retroactive Backdating (MySQL timestamp rewrites)",
        "Score Collusion (Quiet score inflation behind closed doors)",
        "Zero Mathematical Proof ('That is what our database recorded')"
    ]
    for itm in items_bad:
        p_t = tfl.add_paragraph()
        p_t.text = "• " + itm
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = C_WHITE

    # Right Card: Cryptographic Solana Reality
    add_card(s2, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.8), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tfr = s2.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(4.9), Inches(4.4)).text_frame
    tfr.word_wrap = True
    pr = tfr.paragraphs[0]
    pr.text = "✔  BidTrace on Solana Anchor"
    pr.font.size = Pt(20)
    pr.font.bold = True
    pr.font.color.rgb = C_CYAN

    items_good = [
        "Consensus Clock Boundary (Slot > deadline = REJECTED)",
        "Dual-Envelope Sealing (Zero pre-deadline price leakage)",
        "Olympic Trimmed Mean (On-chain rogue score auto-pruning)",
        "Air-Gapped Tribunal Verifier (100% offline mathematical proof)"
    ]
    for itm in items_good:
        p_t = tfr.add_paragraph()
        p_t.text = "• " + itm
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = C_CYAN

    s2.notes_slide.notes_text_frame.text = (
        "[SLIDE 2 | 0:15 - 0:40 | 54 Words]\n"
        "\"The fatal flaw in procurement isn't bad people—it's a physical window of time. "
        "Between the deadline and bid opening, database admins have god-mode. "
        "They peek at competitor pricing, alter scores, and backdate late bids into MySQL databases. "
        "BidTrace replaces administrative custody with Solana's consensus clock: "
        "if a slot expires, code blocks entry forever.\""
    )

    # =========================================================================
    # SLIDE 3: TWO-PLANE ARCHITECTURE (CLEAN COLUMNS, NO PARAGRAPHS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)

    th3 = s3.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf3 = th3.text_frame
    p = tf3.paragraphs[0]
    p.text = "PROTOCOL ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf3.add_paragraph()
    p2.text = "Two-Plane Decoupled Architecture"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    planes = [
        ("1. SEMANTIC PLANE", "Off-Chain Standard", [
            "OCDS 1.1 Compliance (World Bank / UN Standard)",
            "RFC 8785 (JCS) Deterministic Hashing",
            "100% Cross-Language Hash Parity",
            "Direct ERP Ingestion (SAP & Oracle)"
        ], C_CYAN),
        ("2. ENFORCEMENT PLANE", "Solana Anchor Engine", [
            "10 Anchor Rust Instructions Deployed",
            "Temporal Slot Clock Hardening",
            "Dual-Envelope PDA State Machine",
            "Commercial Secrecy Invariant (Locked Forever)"
        ], C_PURPLE),
        ("3. GATEWAY PLANE", "Zero-Fiat-Gas Relayer", [
            "Zero Crypto Gas for Contractors",
            "4 Hybrid Bond Registry Modes",
            "SWIFT MT760 & TradFi Surety Integration",
            "Air-Gapped Tribunal Dossier Verifier"
        ], C_EMERALD)
    ]

    for i, (title, sub, bullets, accent) in enumerate(planes):
        cx = Inches(1.0 + i * 3.85)
        add_card(s3, cx, Inches(1.9), Inches(3.6), Inches(4.8))
        tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(2.1), Inches(3.2), Inches(4.4))
        tf_c = tb.text_frame
        tf_c.word_wrap = True
        pt = tf_c.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = accent
        ps = tf_c.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT_MUTED
        tf_c.add_paragraph()

        for b in bullets:
            pb = tf_c.add_paragraph()
            pb.text = "▪ " + b
            pb.font.size = Pt(13)
            pb.font.color.rgb = C_WHITE

    s3.notes_slide.notes_text_frame.text = (
        "[SLIDE 3 | 0:40 - 1:05 | 55 Words]\n"
        "\"To solve this without forcing governments to hold crypto, we built a two-plane architecture. "
        "Off-chain, we serialize tenders using the World Bank's OCDS 1.1 standard and RFC 8785 canonical hashing. "
        "On-chain, ten Solana Anchor instructions enforce temporal phase locks, blinded evaluator rubrics, "
        "and commercial secrecy—sponsored by a zero-fiat-gas relayer.\""
    )

    # =========================================================================
    # SLIDE 4: 4-STAGE LIFECYCLE & LIVE DEFENSES (ACTIONABLE TILES)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)

    th4 = s4.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf4 = th4.text_frame
    p = tf4.paragraphs[0]
    p.text = "END-TO-END CRYPTOGRAPHIC PIPELINE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p2 = tf4.add_paragraph()
    p2.text = "The 4-Stage Lifecycle & Tested Adversarial Defenses"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # 4 Minimal Step Tiles
    steps = [
        ("STAGE 1", "Tender Issued", "Canonical OCDS Notice + Slot Cutoff", C_CYAN),
        ("STAGE 2", "Dual-Envelopes", "Blinded Technical & Financial Bids", C_PURPLE),
        ("STAGE 3", "Blinded Scoring", "Olympic Trimmed Mean Outlier Pruning", C_AMBER),
        ("STAGE 4", "QCBS Award", "Qualified Unseal & Deterministic Winner", C_EMERALD)
    ]
    for i, (stg, stitle, sdesc, scol) in enumerate(steps):
        sx = Inches(1.0 + i * 2.88)
        add_card(s4, sx, Inches(1.9), Inches(2.7), Inches(2.0))
        tbs = s4.shapes.add_textbox(sx + Inches(0.15), Inches(2.0), Inches(2.4), Inches(1.8)).text_frame
        tbs.word_wrap = True
        p1 = tbs.paragraphs[0]
        p1.text = stg
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = scol
        p2 = tbs.add_paragraph()
        p2.text = stitle
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tbs.add_paragraph()
        p3.text = sdesc
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom Banner: 4 Tested Adversarial Attacks Rejected On-Chain
    add_card(s4, Inches(1.0), Inches(4.15), Inches(11.33), Inches(2.75))
    tb_def = s4.shapes.add_textbox(Inches(1.2), Inches(4.25), Inches(10.9), Inches(2.55))
    tf_def = tb_def.text_frame
    tf_def.word_wrap = True
    p_def = tf_def.paragraphs[0]
    p_def.text = "TESTED ADVERSARIAL ATTACKS REJECTED ON SOLANA DEVNET"
    p_def.font.size = Pt(13)
    p_def.font.bold = True
    p_def.font.color.rgb = C_ROSE

    attacks = [
        ("Late Bidder Injected", "Anchor Error: SubmissionDeadlineExceeded (0x1773)"),
        ("Price Tampering (-$500k)", "Anchor Error: InvalidRevealHash (0x1775)"),
        ("Rogue Judge 98% Score", "On-Chain Filter: OlympicTrimmedMeanPruned"),
        ("Trade Secret Leak", "Anchor Error: CommercialSecrecyLock")
    ]
    for att, res in attacks:
        p_row = tf_def.add_paragraph()
        p_row.text = f"🛑  {att}  ➔  {res}"
        p_row.font.size = Pt(13)
        p_row.font.color.rgb = C_WHITE

    s4.notes_slide.notes_text_frame.text = (
        "[SLIDE 4 | 1:05 - 1:30 | 56 Words]\n"
        "\"Here is the live lifecycle. Stage 1: Tenders are published with canonical hashes. "
        "Stage 2: Contractors seal dual envelopes. Stage 3: Evaluators grade blindly, "
        "and our on-chain trimmed mean automatically prunes rogue scores. "
        "Stage 4: Only qualified bids unseal price. "
        "In our attack simulator, late bids, price tampering, and data leaks get rejected on-chain.\""
    )

    # =========================================================================
    # SLIDE 5: WHY SOLANA (3 CLEAN METRIC PILLARS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)

    th5 = s5.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf5 = th5.text_frame
    p = tf5.paragraphs[0]
    p.text = "THE SOLANA ADVANTAGE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p2 = tf5.add_paragraph()
    p2.text = "Why Solana is Structurally Required"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    sol_pillars = [
        ("400ms Proof of History", "Temporal Finality", [
            "Sub-second statutory cutoff precision",
            "Zero retroactive block jitter or timestamp edits",
            "Mathematical guarantee over historical slots"
        ], C_CYAN),
        ("Micro-Cent Network Fees", "Granular State Updates", [
            "5-stage multi-envelope state transitions",
            "5 evaluator score commits per tender",
            "< $0.01 total gas per entire tender lifecycle"
        ], C_PURPLE),
        ("Zero-Gas Gateway", "Frictionless TradFi Adoption", [
            "Zero crypto balance required for contractors",
            "Sponsored relayer pays all network gas",
            "100% compliant with sovereign treasury laws"
        ], C_EMERALD)
    ]

    for i, (title, sub, bullets, accent) in enumerate(sol_pillars):
        cx = Inches(1.0 + i * 3.85)
        add_card(s5, cx, Inches(1.9), Inches(3.6), Inches(4.8))
        tb = s5.shapes.add_textbox(cx + Inches(0.2), Inches(2.1), Inches(3.2), Inches(4.4))
        tf_c = tb.text_frame
        tf_c.word_wrap = True
        pt = tf_c.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(17)
        pt.font.bold = True
        pt.font.color.rgb = accent
        ps = tf_c.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT_MUTED
        tf_c.add_paragraph()

        for b in bullets:
            pb = tf_c.add_paragraph()
            pb.text = "▪ " + b
            pb.font.size = Pt(13)
            pb.font.color.rgb = C_WHITE

    s5.notes_slide.notes_text_frame.text = (
        "[SLIDE 5 | 1:30 - 1:50 | 44 Words]\n"
        "\"Why Solana? Two reasons: Proof of History and cost. "
        "Solana's 400-millisecond slot clock provides the sub-second temporal certainty required to legally freeze bids. "
        "And because transactions cost fractions of a cent, our relayer sponsors all gas, "
        "allowing governments to adopt Web3 guarantees without holding volatile crypto.\""
    )

    # =========================================================================
    # SLIDE 6: TRACTION & ASK (BIG STATS, CLEAN CTAS)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)

    th6 = s6.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf6 = th6.text_frame
    p = tf6.paragraphs[0]
    p.text = "VERIFIED EXECUTION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf6.add_paragraph()
    p2.text = "Shipped, Tested, and Verified on Solana Devnet"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # 4 Big Stat Numbers
    stat_boxes = [
        ("10", "Anchor Instructions", "Deployed on Devnet", C_CYAN),
        ("78 / 78", "Passing Unit Tests", "100% Hash Parity", C_EMERALD),
        ("5 / 5", "Storyboard Steps", "1-Click Interactive HUD", C_PURPLE),
        ("4", "Hybrid Bond Modes", "TradFi + Crypto", C_AMBER)
    ]
    for i, (num, title, sub, col) in enumerate(stat_boxes):
        ax = Inches(1.0 + i * 2.88)
        add_card(s6, ax, Inches(1.9), Inches(2.7), Inches(2.1))
        tb_a = s6.shapes.add_textbox(ax + Inches(0.15), Inches(2.0), Inches(2.4), Inches(1.9))
        tfa = tb_a.text_frame
        tfa.word_wrap = True
        p1 = tfa.paragraphs[0]
        p1.text = num
        p1.font.size = Pt(32)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tfa.add_paragraph()
        p2.text = title
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tfa.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom Link Box
    add_card(s6, Inches(1.0), Inches(4.35), Inches(11.33), Inches(2.45), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tfc = s6.shapes.add_textbox(Inches(1.3), Inches(4.55), Inches(10.7), Inches(2.1)).text_frame
    tfc.word_wrap = True
    pc1 = tfc.paragraphs[0]
    pc1.text = "THE SETTLEMENT LAYER FOR SOVEREIGN CAPITAL"
    pc1.font.size = Pt(15)
    pc1.font.bold = True
    pc1.font.color.rgb = C_CYAN
    pc2 = tfc.add_paragraph()
    pc2.text = "Live Interactive Web App: bidtrace.net"
    pc2.font.size = Pt(20)
    pc2.font.bold = True
    pc2.font.color.rgb = C_WHITE
    pc3 = tfc.add_paragraph()
    pc3.text = "Program ID: x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ  |  GitHub: Ujjwal1396/BidTrace"
    pc3.font.size = Pt(13)
    pc3.font.color.rgb = C_TEXT_MUTED

    s6.notes_slide.notes_text_frame.text = (
        "[SLIDE 6 | 1:50 - 2:00 | 25 Words]\n"
        "\"BidTrace is fully functional today: live on Solana Devnet, backed by 78 passing unit tests and a live web app at bidtrace.net. "
        "Thank you!\""
    )

    out_file = "BidTrace_Pitch_Deck_2Min.pptx"
    prs.save(out_file)
    prs.save("public/" + out_file)
    print("Clean, minimalist deck saved to BidTrace_Pitch_Deck_2Min.pptx and public/!")

if __name__ == "__main__":
    create_deck()
