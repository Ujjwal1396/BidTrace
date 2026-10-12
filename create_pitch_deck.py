import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette
    C_BG = RGBColor(10, 15, 29)          # Deep Midnight #0A0F1D
    C_CARD = RGBColor(18, 25, 45)        # Slate Card #12192D
    C_CARD_BORDER = RGBColor(30, 41, 70) # Subtle Card Border #1E2946
    C_WHITE = RGBColor(255, 255, 255)
    C_CYAN = RGBColor(6, 182, 212)       # Electric Cyan #06B6D4
    C_PURPLE = RGBColor(168, 85, 247)    # Purple Accent #A855F7
    C_TEXT_MUTED = RGBColor(148, 163, 184) # Slate Muted #94A3B8
    C_ROSE = RGBColor(244, 63, 94)       # Danger Rose #F43F5E
    C_EMERALD = RGBColor(16, 185, 129)   # Success Emerald #10B981
    C_AMBER = RGBColor(245, 158, 11)     # Warning Amber #F59E0B

    logo_path = os.path.abspath("public/logo-mark.png")
    hero_img = os.path.abspath(r"C:\Users\ujjwa\.gemini\antigravity\brain\51e8fc02-9aef-46d0-b935-81bb4c75dcff\winning_oneliner_hero.png")
    attack_img = os.path.abspath(r"C:\Users\ujjwa\.gemini\antigravity\brain\51e8fc02-9aef-46d0-b935-81bb4c75dcff\step3_attack_modal.png")
    award_img = os.path.abspath(r"C:\Users\ujjwa\.gemini\antigravity\brain\51e8fc02-9aef-46d0-b935-81bb4c75dcff\step5_clean_award.png")

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
    # SLIDE 1: TITLE / HOOK (0:00 - 0:15)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Logo Emblem
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(1.2), Inches(1.8), width=Inches(1.6))

    # Badge: Colosseum Crypto World's Fair
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(1.85), Inches(3.8), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(16, 32, 55)
    badge.line.color.rgb = C_CYAN
    badge.text_frame.text = "COLOSSEUM CRYPTO WORLD'S FAIR 2026"
    badge.text_frame.paragraphs[0].font.size = Pt(11)
    badge.text_frame.paragraphs[0].font.bold = True
    badge.text_frame.paragraphs[0].font.color.rgb = C_CYAN
    badge.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(3.1), Inches(2.35), Inches(9.2), Inches(1.5))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "BidTrace"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Headline
    tb_sub = s1.shapes.add_textbox(Inches(1.2), Inches(3.9), Inches(11.0), Inches(1.2))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Tamper-Proof Sealed Bidding for Public Contracts on Solana"
    p_sub.font.size = Pt(28)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_CYAN

    # Subtitle
    p_sub2 = tf_sub.add_paragraph()
    p_sub2.text = "Eliminating the $13 Trillion Post-Deadline Insider Tampering Window via Solana Anchor PDA State Machines & OCDS 1.1 Canonical Hashing."
    p_sub2.font.size = Pt(16)
    p_sub2.font.color.rgb = C_TEXT_MUTED

    # Bottom 3 Stat Badges
    b_data = [
        ("$13.0 Trillion", "Protected Market (15-20% Global GDP)"),
        ("400ms Sub-Second", "Solana Consensus Clock Boundary"),
        ("Zero Crypto Gas", "Sponsored Relayer for Enterprise Contractors")
    ]
    for i, (val, desc) in enumerate(b_data):
        b_x = Inches(1.2 + i * 3.75)
        add_card(s1, b_x, Inches(5.5), Inches(3.5), Inches(1.2))
        t_box = s1.shapes.add_textbox(b_x + Inches(0.2), Inches(5.55), Inches(3.1), Inches(1.1))
        tf_b = t_box.text_frame
        p_val = tf_b.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(20)
        p_val.font.bold = True
        p_val.font.color.rgb = C_CYAN if i==0 else (C_PURPLE if i==1 else C_EMERALD)
        p_desc = tf_b.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "[SLIDE 1 | 0:00 - 0:15 | 32 Words]\n"
        "\"Judges, every year, $13 trillion is spent on public infrastructure. "
        "Yet the entire industry relies on centralized database trust. "
        "BidTrace brings tamper-proof sealed bidding to public contracts on Solana, "
        "making corruption mathematically impossible.\""
    )

    # =========================================================================
    # SLIDE 2: THE $13T PROBLEM: THE INSIDER TAMPERING WINDOW (0:15 - 0:40)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)

    # Section Header
    th2 = s2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.9))
    tf2 = th2.text_frame
    p = tf2.paragraphs[0]
    p.text = "THE $13 TRILLION CRITICAL FAILURE POINT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p2 = tf2.add_paragraph()
    p2.text = "The Post-Deadline Insider Exploitation Window"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # Card Left: Traditional E-Procurement Vulnerability
    c_left = add_card(s2, Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.8))
    tfl = s2.shapes.add_textbox(Inches(1.3), Inches(2.0), Inches(4.8), Inches(4.4)).text_frame
    tfl.word_wrap = True
    pl1 = tfl.paragraphs[0]
    pl1.text = "Centralized Web2 Portals (SAP, Oracle, e-GP)"
    pl1.font.size = Pt(18)
    pl1.font.bold = True
    pl1.font.color.rgb = C_ROSE

    bullets_trad = [
        ("The Insider Peek Window:", "Between submission closing and bid opening, centralized database administrators have total root access to view unencrypted competitor pricing."),
        ("Retroactive Backdating:", "Corrupt officials insert favored contractors 5 minutes after the deadline by backdating server database timestamps."),
        ("Subjective Grade Alterations:", "Evaluators quietly rewrite technical proposal scores behind closed doors to favor political cronies."),
        ("The 'God-Mode' Excuse:", "When challenged, agencies point to their server logs: 'That is what our database recorded.' There is zero cryptographic proof.")
    ]
    for b_title, b_body in bullets_trad:
        p_t = tfl.add_paragraph()
        p_t.text = "✖  " + b_title
        p_t.font.bold = True
        p_t.font.size = Pt(13)
        p_t.font.color.rgb = C_WHITE
        p_b = tfl.add_paragraph()
        p_b.text = "    " + b_body
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_TEXT_MUTED

    # Card Right: What Solves It
    c_right = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.5), Inches(4.8), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tfr = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(4.9), Inches(4.4)).text_frame
    tfr.word_wrap = True
    pr1 = tfr.paragraphs[0]
    pr1.text = "The Cryptographic Reality Check"
    pr1.font.size = Pt(18)
    pr1.font.bold = True
    pr1.font.color.rgb = C_CYAN

    bullets_sol = [
        ("Immutable Clock Boundary:", "Solana Anchor PDA verifies Clock::get()?.slot <= deadline_slot. Once slot 1050 passes, zero administrative keys can inject a bid."),
        ("Blind Dual Commitments:", "Envelope A (Technical) & Envelope B (Financial) are hashed with preimages. Pricing remains strictly sealed until evaluation is finalized."),
        ("Olympic Trimmed Mean:", "On-chain algorithm discards extreme high/low evaluator grades and automatically flags rogue collusion on-chain."),
        ("Air-Gapped Tribunal Verifier:", "Anyone can audit the entire procurement lifecycle offline directly against raw Solana account proofs.")
    ]
    for b_title, b_body in bullets_sol:
        p_t = tfr.add_paragraph()
        p_t.text = "✔  " + b_title
        p_t.font.bold = True
        p_t.font.size = Pt(13)
        p_t.font.color.rgb = C_CYAN
        p_b = tfr.add_paragraph()
        p_b.text = "    " + b_body
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_TEXT_MUTED

    s2.notes_slide.notes_text_frame.text = (
        "[SLIDE 2 | 0:15 - 0:40 | 54 Words]\n"
        "\"The fatal flaw in procurement isn't bad people—it's a physical window of time. "
        "Between the deadline and bid opening, database admins have god-mode. "
        "They peek at competitor pricing, alter scores, and backdate late bids into MySQL databases. "
        "BidTrace replaces administrative custody with Solana's consensus clock: "
        "if a slot expires, code blocks entry forever.\""
    )

    # =========================================================================
    # SLIDE 3: THE SOLUTION ARCHITECTURE (0:40 - 1:05)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)

    th3 = s3.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.9))
    tf3 = th3.text_frame
    p = tf3.paragraphs[0]
    p.text = "PROTOCOL ARCHITECTURE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf3.add_paragraph()
    p2.text = "The Incorruptible Two-Plane State Machine"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # 3 Architecture Pillars Cards
    arch_cols = [
        ("1. SEMANTIC PLANE", "Off-Chain Open Contracting", [
            ("OCDS 1.1 Compliant:", "Canonical tender JSON data standard adopted by the World Bank and UN."),
            ("RFC 8785 JCS Hashing:", "Deterministic JSON Canonicalization Scheme produces identical cross-language SHA-256 anchors."),
            ("TradFi Interoperability:", "Existing government ERPs (SAP, Oracle) export standard OCDS notices directly.")
        ], C_CYAN),
        ("2. ENFORCEMENT PLANE", "On-Chain Solana Anchor Engine", [
            ("PDA State Machine:", "10 Rust instructions strictly gate phase transitions (Bidding -> Technical -> Financial -> Award)."),
            ("Temporal Slot Hardening:", "Slot boundaries are validated directly against Solana's Proof of History clock."),
            ("Commercial Secrecy Lock:", "Disqualified bidders (score < 75%) are permanently prevented on-chain from unsealing financial prices.")
        ], C_PURPLE),
        ("3. GATEWAY PLANE", "Zero-Fiat-Gas Enterprise Relayer", [
            ("Gas Decoupling:", "Government agencies and contractors pay zero SOL. All network fees are sponsored by the backend relayer."),
            ("Hybrid Bond Registry:", "Supports native Solana Escrow, TradFi Surety policies, SWIFT MT760 guarantees, and World Bank BSDs."),
            ("Offline Auditability:", "Standalone Python & Node.js verifier checks cryptographic proofs air-gapped.")
        ], C_EMERALD)
    ]

    for i, (title, sub, bullets, accent) in enumerate(arch_cols):
        cx = Inches(1.0 + i * 3.85)
        add_card(s3, cx, Inches(1.8), Inches(3.6), Inches(5.0))
        tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(2.0), Inches(3.2), Inches(4.6))
        tf_c = tb.text_frame
        tf_c.word_wrap = True
        pt = tf_c.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = accent
        ps = tf_c.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT_MUTED
        tf_c.add_paragraph() # spacer

        for b_name, b_desc in bullets:
            pb_name = tf_c.add_paragraph()
            pb_name.text = "▪ " + b_name
            pb_name.font.size = Pt(12)
            pb_name.font.bold = True
            pb_name.font.color.rgb = C_WHITE
            pb_desc = tf_c.add_paragraph()
            pb_desc.text = "  " + b_desc
            pb_desc.font.size = Pt(10)
            pb_desc.font.color.rgb = C_TEXT_MUTED

    s3.notes_slide.notes_text_frame.text = (
        "[SLIDE 3 | 0:40 - 1:05 | 55 Words]\n"
        "\"To solve this without forcing governments to hold crypto, we built a two-plane architecture. "
        "Off-chain, we serialize tenders using the World Bank's OCDS 1.1 standard and RFC 8785 canonical hashing. "
        "On-chain, ten Solana Anchor instructions enforce temporal phase locks, blinded evaluator rubrics, "
        "and commercial secrecy—sponsored by a zero-fiat-gas relayer.\""
    )

    # =========================================================================
    # SLIDE 4: THE 4-STAGE LIFECYCLE & LIVE ATTACK DEFENSE (1:05 - 1:30)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)

    th4 = s4.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.9))
    tf4 = th4.text_frame
    p = tf4.paragraphs[0]
    p.text = "HOW IT WORKS IN PRACTICE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p2 = tf4.add_paragraph()
    p2.text = "The 4-Stage Incorruptible Lifecycle & Adversarial Defense"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # 4 Steps Horizontal Flow
    steps_data = [
        ("STAGE 1", "Tender Publication", "Authority issues RFP with canonical OCDS hash and fixed deadline slot.", C_CYAN),
        ("STAGE 2", "Dual Sealed Commit", "Bidders commit Envelope A (specs) and Envelope B (pricing) independently.", C_PURPLE),
        ("STAGE 3", "Blinded Scoring", "5 evaluators grade proposals; Olympic Trimmed Mean prunes rogue outliers.", C_AMBER),
        ("STAGE 4", "QCBS Final Award", "Only qualified bids unseal Envelope B. Award computed deterministically.", C_EMERALD)
    ]
    for i, (stg, stitle, sbody, scol) in enumerate(steps_data):
        sx = Inches(1.0 + i * 2.88)
        add_card(s4, sx, Inches(1.8), Inches(2.7), Inches(2.3))
        tb_s = s4.shapes.add_textbox(sx + Inches(0.15), Inches(1.9), Inches(2.4), Inches(2.1))
        tfs = tb_s.text_frame
        tfs.word_wrap = True
        p1 = tfs.paragraphs[0]
        p1.text = stg
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = scol
        p2 = tfs.add_paragraph()
        p2.text = stitle
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tfs.add_paragraph()
        p3.text = sbody
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom Split: 4 Adversarial Defenses Matrix
    add_card(s4, Inches(1.0), Inches(4.35), Inches(11.33), Inches(2.55))
    tb_def = s4.shapes.add_textbox(Inches(1.2), Inches(4.45), Inches(10.9), Inches(2.35))
    tf_def = tb_def.text_frame
    tf_def.word_wrap = True
    p_def_head = tf_def.paragraphs[0]
    p_def_head.text = "TESTED ADVERSARIAL ATTACKS REJECTED ON SOLANA DEVNET"
    p_def_head.font.size = Pt(12)
    p_def_head.font.bold = True
    p_def_head.font.color.rgb = C_ROSE

    def_items = [
        ("Attack 1: Late Bid Injection", "Adversary injects bid at slot > 1050.", "Anchor rejects: SubmissionDeadlineExceeded (0x1773)."),
        ("Attack 2: Price Tampering", "Insider alters quotation from $3.8M to $3.3M.", "Anchor rejects: InvalidRevealHash (0x1775)."),
        ("Attack 3: Evaluator Collusion", "Corrupt judge submits 98% outlier score.", "Olympic Trimmed Mean discards score & flags judge."),
        ("Attack 4: Trade Secret Espionage", "Buyer attempts to leak disqualified Bidder B's pricing.", "Anchor bars reveal: BidderTechnicallyDisqualified.")
    ]
    for att, act, out in def_items:
        p_row = tf_def.add_paragraph()
        p_row.text = f"🛑 {att}: {act} ➔ {out}"
        p_row.font.size = Pt(11)
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
    # SLIDE 5: WHY SOLANA & TRADFI ADOPTION (1:30 - 1:50)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)

    th5 = s5.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.9))
    tf5 = th5.text_frame
    p = tf5.paragraphs[0]
    p.text = "WHY SOLANA IS ESSENTIAL"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p2 = tf5.add_paragraph()
    p2.text = "The Consensus Clock & Micro-Fee Advantage"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    sol_cards = [
        ("400ms Proof of History Clock", "Strict Temporal Enforcement", [
            "Traditional blockchains have 12-second block jitter.",
            "Solana's 400ms slot finality provides sub-second proof of exact submission cutoff times.",
            "Historical slots cannot be retroactively modified by validators or admins."
        ], C_CYAN),
        ("Sub-Cent High Frequency Fees", "Granular Multi-Envelope Commitments", [
            "Tenders generate dozens of granular state updates: envelope commits, 5 evaluator scores, unseals.",
            "EVM gas costs ($10-$50) make multi-round commits economically unviable.",
            "Solana executes the full 5-stage lifecycle for < $0.01 total network gas."
        ], C_PURPLE),
        ("TradFi Decoupling Gateway", "Institutional Adoption Today", [
            "Zero crypto balance required for corporate treasuries.",
            "Multi-jurisdiction bond engine: Surety MGA policies, SWIFT MT760 bank guarantees, World Bank BSDs.",
            "Full compatibility with existing e-GP legal frameworks (FIDIC & World Bank)."
        ], C_EMERALD)
    ]

    for i, (stitle, ssub, sbullets, scol) in enumerate(sol_cards):
        cx = Inches(1.0 + i * 3.85)
        add_card(s5, cx, Inches(1.8), Inches(3.6), Inches(5.0))
        tb_sc = s5.shapes.add_textbox(cx + Inches(0.2), Inches(2.0), Inches(3.2), Inches(4.6))
        tf_sc = tb_sc.text_frame
        tf_sc.word_wrap = True
        pt = tf_sc.paragraphs[0]
        pt.text = stitle
        pt.font.size = Pt(15)
        pt.font.bold = True
        pt.font.color.rgb = scol
        ps = tf_sc.add_paragraph()
        ps.text = ssub
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT_MUTED
        tf_sc.add_paragraph()

        for b in sbullets:
            pb = tf_sc.add_paragraph()
            pb.text = "▪ " + b
            pb.font.size = Pt(11)
            pb.font.color.rgb = C_WHITE

    s5.notes_slide.notes_text_frame.text = (
        "[SLIDE 5 | 1:30 - 1:50 | 44 Words]\n"
        "\"Why Solana? Two reasons: Proof of History and cost. "
        "Solana's 400-millisecond slot clock provides the sub-second temporal certainty required to legally freeze bids. "
        "And because transactions cost fractions of a cent, our relayer sponsors all gas, "
        "allowing governments to adopt Web3 guarantees without holding volatile crypto.\""
    )

    # =========================================================================
    # SLIDE 6: TRACTION, LIVE DEMO & THE VISION (1:50 - 2:00)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)

    th6 = s6.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.9))
    tf6 = th6.text_frame
    p = tf6.paragraphs[0]
    p.text = "WHAT WE BUILT & TRACTION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf6.add_paragraph()
    p2.text = "Shipped, Tested, and Verified on Solana Devnet"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # 4 Achievement Cards
    achievements = [
        ("Anchor Devnet Deployed", "Live Program", "x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ on Devnet cluster.", C_CYAN),
        ("78 Passing Unit Tests", "100% Cryptographic Parity", "Full Python and Node.js cross-language RFC 8785 hash parity verified.", C_EMERALD),
        ("Live Web Dashboard", "bidtrace.net", "Full interactive 5-step storyboard HUD, 7 portals, and attack simulator.", C_PURPLE),
        ("Air-Gapped Verifier", "Independent Tribunal", "Complete Python dossier verifier for offline legal audits.", C_AMBER)
    ]
    for i, (atitle, asub, abody, acol) in enumerate(achievements):
        ax = Inches(1.0 + i * 2.88)
        add_card(s6, ax, Inches(1.8), Inches(2.7), Inches(2.4))
        tb_a = s6.shapes.add_textbox(ax + Inches(0.15), Inches(1.9), Inches(2.4), Inches(2.2))
        tfa = tb_a.text_frame
        tfa.word_wrap = True
        p1 = tfa.paragraphs[0]
        p1.text = atitle
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = acol
        p2 = tfa.add_paragraph()
        p2.text = asub
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tfa.add_paragraph()
        p3.text = abody
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom Hero Callout
    add_card(s6, Inches(1.0), Inches(4.5), Inches(11.33), Inches(2.3), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tb_c = s6.shapes.add_textbox(Inches(1.3), Inches(4.7), Inches(10.7), Inches(1.9))
    tfc = tb_c.text_frame
    tfc.word_wrap = True
    pc1 = tfc.paragraphs[0]
    pc1.text = "THE VISION: THE TRUSTED SETTLEMENT LAYER FOR GLOBAL CAPITAL"
    pc1.font.size = Pt(14)
    pc1.font.bold = True
    pc1.font.color.rgb = C_CYAN
    pc2 = tfc.add_paragraph()
    pc2.text = "Public procurement is 15% of global GDP. By establishing mathematical finality over bid intake, evaluator scoring, and award execution, BidTrace is building the incorruptible cryptographic operating system for sovereign infrastructure."
    pc2.font.size = Pt(13)
    pc2.font.color.rgb = C_WHITE
    pc3 = tfc.add_paragraph()
    pc3.text = "Explore the live dashboard at bidtrace.net | GitHub: github.com/Ujjwal1396/BidTrace"
    pc3.font.size = Pt(12)
    pc3.font.bold = True
    pc3.font.color.rgb = C_CYAN

    s6.notes_slide.notes_text_frame.text = (
        "[SLIDE 6 | 1:50 - 2:00 | 25 Words]\n"
        "\"BidTrace is fully functional today: live on Solana Devnet, backed by 78 passing unit tests and a live web app at bidtrace.net. "
        "Thank you!\""
    )

    out_file = "BidTrace_Pitch_Deck_2Min.pptx"
    prs.save(out_file)
    print(f"Presentation saved successfully to {out_file}!")

if __name__ == "__main__":
    create_deck()
