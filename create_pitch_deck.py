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

    # Theme Colors (Dark Slate / Cyber Midnight)
    C_BG = RGBColor(10, 15, 29)          # Deep Midnight (#0a0f1d)
    C_CARD = RGBColor(18, 25, 45)        # Card Background (#12192d)
    C_CARD_BORDER = RGBColor(30, 41, 70) # Subtle Border (#1e2946)
    C_WHITE = RGBColor(255, 255, 255)
    C_CYAN = RGBColor(6, 182, 212)       # Electric Cyan (#06b6d4)
    C_PURPLE = RGBColor(168, 85, 247)    # Purple (#a855f7)
    C_TEXT_MUTED = RGBColor(148, 163, 184) # Muted Grey (#94a3b8)
    C_ROSE = RGBColor(244, 63, 94)       # Danger Rose (#f43f5e)
    C_EMERALD = RGBColor(16, 185, 129)   # Emerald (#10b981)
    C_AMBER = RGBColor(245, 158, 11)     # Amber (#f59e0b)

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
    # SLIDE 1: COVER SLIDE (Winning One-Liner, <40 words)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(1.2), Inches(1.5), width=Inches(1.8))

    # Event Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), Inches(1.55), Inches(4.2), Inches(0.42))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(16, 32, 55)
    b1.line.color.rgb = C_CYAN
    b1.text_frame.text = "COLOSSEUM CRYPTO WORLD'S FAIR 2026"
    b1.text_frame.paragraphs[0].font.size = Pt(11)
    b1.text_frame.paragraphs[0].font.bold = True
    b1.text_frame.paragraphs[0].font.color.rgb = C_CYAN
    b1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Brand Title
    tb_title = s1.shapes.add_textbox(Inches(3.2), Inches(2.05), Inches(9.0), Inches(1.2))
    p = tb_title.text_frame.paragraphs[0]
    p.text = "BidTrace"
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Big Winning Headline
    tb_h = s1.shapes.add_textbox(Inches(1.2), Inches(3.45), Inches(11.0), Inches(1.5))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "No More Bid Rigging."
    p_h.font.size = Pt(36)
    p_h.font.bold = True
    p_h.font.color.rgb = C_CYAN
    p_sub = tf_h.add_paragraph()
    p_sub.text = "Cryptographic sealed bidding for public infrastructure contracts."
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = C_TEXT_MUTED

    # 3 Stat Cards
    stats_s1 = [
        ("$13.0 Trillion", "Annual Sovereign Spend", C_CYAN),
        ("400ms Clock", "Proof of History Precision", C_PURPLE),
        ("Zero Crypto Gas", "Enterprise Relayer Sponsored", C_EMERALD)
    ]
    for i, (num, lbl, col) in enumerate(stats_s1):
        bx = Inches(1.2 + i * 3.75)
        add_card(s1, bx, Inches(5.2), Inches(3.5), Inches(1.5))
        tb_st = s1.shapes.add_textbox(bx + Inches(0.2), Inches(5.35), Inches(3.1), Inches(1.2))
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
        "[SLIDE 1 | 0:00 - 0:15 | 24 Words on Slide]\n"
        "\"Judges, every year $13 trillion is spent on public infrastructure, "
        "yet bid rigging and database tampering steal up to 25% of that capital. "
        "BidTrace eliminates bid rigging with cryptographic sealed bidding on Solana, "
        "turning administrative trust into mathematical certainty.\""
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM (Face-Punch Stat + Human Angle, <40 words)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)

    th2 = s2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf2 = th2.text_frame
    p = tf2.paragraphs[0]
    p.text = "THE $13 TRILLION CRITICAL FLAW"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p2 = tf2.add_paragraph()
    p2.text = "The Post-Deadline Insider Tampering Window"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # Left: Face-Punch Stat Card
    add_card(s2, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.8), bg_color=C_CARD, border_color=RGBColor(80, 20, 35))
    tfl = s2.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(4.8), Inches(4.2)).text_frame
    tfl.word_wrap = True
    pl1 = tfl.paragraphs[0]
    pl1.text = "$13 Trillion / Year"
    pl1.font.size = Pt(36)
    pl1.font.bold = True
    pl1.font.color.rgb = C_ROSE
    pl2 = tfl.add_paragraph()
    pl2.text = "15% of Global GDP Vulnerable to Insider DBA Access"
    pl2.font.size = Pt(16)
    pl2.font.bold = True
    pl2.font.color.rgb = C_WHITE
    pl3 = tfl.add_paragraph()
    pl3.text = "\n• Database admins hold MySQL root keys.\n• Late bids quietly backdated before opening.\n• Unencrypted prices leaked to favored bidders."
    pl3.font.size = Pt(14)
    pl3.font.color.rgb = C_TEXT_MUTED

    # Right: The Fundamental Flaw
    add_card(s2, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.8), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tfr = s2.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(4.9), Inches(4.2)).text_frame
    tfr.word_wrap = True
    pr1 = tfr.paragraphs[0]
    pr1.text = "Zero Math Proof"
    pr1.font.size = Pt(36)
    pr1.font.bold = True
    pr1.font.color.rgb = C_CYAN
    pr2 = tfr.add_paragraph()
    pr2.text = "Centralized Trust Fails Daily in E-Procurement"
    pr2.font.size = Pt(16)
    pr2.font.bold = True
    pr2.font.color.rgb = C_WHITE
    pr3 = tfr.add_paragraph()
    pr3.text = "\n• Server timestamps rewritten in seconds.\n• Rogue evaluator scores inflated behind closed doors.\n• Admins claim: 'That is what our database recorded.'"
    pr3.font.size = Pt(14)
    pr3.font.color.rgb = C_TEXT_MUTED

    s2.notes_slide.notes_text_frame.text = (
        "[SLIDE 2 | 0:15 - 0:35 | 38 Words on Slide]\n"
        "\"The fatal flaw in procurement isn't bad people—it's a window of time. "
        "Between the submission deadline and bid opening, database admins have unmonitored root access "
        "to peek at competitor pricing, alter scores, and backdate bids in MySQL. "
        "Traditional audits fail because centralized databases produce zero mathematical proof.\""
    )

    # =========================================================================
    # SLIDE 3: SOLUTION (Product as Hero + Analogy, <40 words)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)

    th3 = s3.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf3 = th3.text_frame
    p = tf3.paragraphs[0]
    p.text = "THE HERO MECHANISM"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf3.add_paragraph()
    p2.text = "“Chainlink + Sealed Envelopes for Sovereign Capital”"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    sol_cards = [
        ("Dual-Envelope Sealing", "OCDS 1.1 Cryptographic Hash", "Blinded technical & financial commitments via RFC 8785 standard. Zero pre-deadline leakage.", C_CYAN),
        ("Proof of History Clock", "Physical Consensus Boundary", "Solana 400ms clock makes post-deadline tampering physically impossible. Expired slots rejected.", C_PURPLE),
        ("Blinded Outlier Pruning", "Olympic Trimmed Mean", "On-chain algorithm auto-prunes collusive evaluator scores before financial unsealing.", C_EMERALD)
    ]
    for i, (title, sub, body, accent) in enumerate(sol_cards):
        cx = Inches(1.0 + i * 3.85)
        add_card(s3, cx, Inches(1.9), Inches(3.6), Inches(4.8))
        tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(2.2), Inches(3.2), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_MUTED
        p3 = tf.add_paragraph()
        p3.text = "\n" + body
        p3.font.size = Pt(14)
        p3.font.color.rgb = C_WHITE

    s3.notes_slide.notes_text_frame.text = (
        "[SLIDE 3 | 0:35 - 0:55 | 37 Words on Slide]\n"
        "\"BidTrace is Chainlink meets sealed envelopes for sovereign infrastructure. "
        "We don't just store hashes; Solana's 400-millisecond Proof of History turns time into an unalterable physical law: "
        "if a slot expires, code rejects entry forever. "
        "Dual envelopes guarantee commercial secrecy, while our on-chain trimmed mean prunes collusive scores.\""
    )

    # =========================================================================
    # SLIDE 4: MARKET OPPORTUNITY (Macro Trends & Dream State, <40 words)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)

    th4 = s4.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf4 = th4.text_frame
    p = tf4.paragraphs[0]
    p.text = "MACRO SHIFT & BOTTOMS-UP BEACHHEAD"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p2 = tf4.add_paragraph()
    p2.text = "From Administrative Paper to Incorruptible Rails"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    add_card(s4, Inches(1.0), Inches(1.9), Inches(5.6), Inches(4.8))
    tf_m = s4.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(5.0), Inches(4.2)).text_frame
    tf_m.word_wrap = True
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Macro Tailwinds & Dream State"
    pm1.font.size = Pt(18)
    pm1.font.bold = True
    pm1.font.color.rgb = C_CYAN
    pm2 = tf_m.add_paragraph()
    pm2.text = "\n• World Bank Mandate: Enforces OCDS 1.1 anti-corruption standard across all projects.\n• TradFi Shift: $500B in multilateral tenders migrating on-chain.\n• Dream State: Incorruptible sovereign infrastructure with zero kickback windows."
    pm2.font.size = Pt(14)
    pm2.font.color.rgb = C_WHITE

    add_card(s4, Inches(7.0), Inches(1.9), Inches(5.3), Inches(2.25), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tft1 = s4.shapes.add_textbox(Inches(7.3), Inches(2.1), Inches(4.7), Inches(1.9)).text_frame
    tft1.word_wrap = True
    pt1 = tft1.paragraphs[0]
    pt1.text = "$500 Billion SAM"
    pt1.font.size = Pt(30)
    pt1.font.bold = True
    pt1.font.color.rgb = C_CYAN
    pt2 = tft1.add_paragraph()
    pt2.text = "Multilateral Development Bank Tenders (Immediate Beachhead)"
    pt2.font.size = Pt(13)
    pt2.font.color.rgb = C_TEXT_MUTED

    add_card(s4, Inches(7.0), Inches(4.45), Inches(5.3), Inches(2.25), bg_color=C_CARD, border_color=C_PURPLE)
    tft2 = s4.shapes.add_textbox(Inches(7.3), Inches(4.65), Inches(4.7), Inches(1.9)).text_frame
    tft2.word_wrap = True
    pt3 = tft2.paragraphs[0]
    pt3.text = "$13.0 Trillion TAM"
    pt3.font.size = Pt(30)
    pt3.font.bold = True
    pt3.font.color.rgb = C_PURPLE
    pt4 = tft2.add_paragraph()
    pt4.text = "Total Annual Global Public Infrastructure Procurement"
    pt4.font.size = Pt(13)
    pt4.font.color.rgb = C_TEXT_MUTED

    s4.notes_slide.notes_text_frame.text = (
        "[SLIDE 4 | 0:55 - 1:15 | 36 Words on Slide]\n"
        "\"The macro tailwind is massive: the World Bank and UN now mandate OCDS 1.1 open data standards "
        "to stop systemic fraud. Our bottoms-up beachhead is the $500 billion in development bank tenders. "
        "The dream state is clear: incorruptible sovereign capital where kickbacks are cryptographically eliminated.\""
    )

    # =========================================================================
    # SLIDE 5: HERO METRICS ("This Is Already Working!", <40 words)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)

    th5 = s5.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf5 = th5.text_frame
    p = tf5.paragraphs[0]
    p.text = "TRACTION & VERIFIED EXECUTION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p2 = tf5.add_paragraph()
    p2.text = "“This Is Already Working Live on Solana”"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    metrics = [
        ("10", "Anchor Instructions", "Deployed on Solana Devnet (x3iSm5BC...ESjZ)", C_CYAN),
        ("78 / 78", "Passing Unit Tests", "100% Cross-Language RFC 8785 Parity", C_EMERALD),
        ("1-Click", "Attack Simulator", "Live On-Chain Exploits Blocked in Real-Time", C_ROSE),
        ("0 Deadlock", "Leaf State Machine", "Rogue bidder default cannot freeze compliant tenders.", C_PURPLE)
    ]
    for i, (num, title, sub, col) in enumerate(metrics):
        mx = Inches(1.0 + i * 2.88)
        add_card(s5, mx, Inches(1.9), Inches(2.7), Inches(4.8))
        tb_m = s5.shapes.add_textbox(mx + Inches(0.15), Inches(2.2), Inches(2.4), Inches(4.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p1 = tf_m.paragraphs[0]
        p1.text = num
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf_m.add_paragraph()
        p2.text = title
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tf_m.add_paragraph()
        p3.text = "\n" + sub
        p3.font.size = Pt(13)
        p3.font.color.rgb = C_TEXT_MUTED

    s5.notes_slide.notes_text_frame.text = (
        "[SLIDE 5 | 1:15 - 1:35 | 38 Words on Slide]\n"
        "\"This is already working live today. We have 10 Anchor Rust instructions deployed on Solana Devnet "
        "and 78 passing unit tests. Crucially, unlike naive auction schemes where one rogue bidder can freeze opening, "
        "our independent leaf architecture and on-chain bond slashing ensure compliant contractors unseal cleanly with zero deadlock.\""
    )

    # =========================================================================
    # SLIDE 6: BUSINESS MODEL ("Why Will This Keep Working!", <40 words)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)

    th6 = s6.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf6 = th6.text_frame
    p = tf6.paragraphs[0]
    p.text = "NETWORK EFFECTS & SUSTAINABLE REVENUE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf6.add_paragraph()
    p2.text = "“Why This Keeps Growing: The Relayer Moat”"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    add_card(s6, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.8), bg_color=C_CARD, border_color=C_CYAN)
    tf_b1 = s6.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(4.8), Inches(4.2)).text_frame
    tf_b1.word_wrap = True
    pb1 = tf_b1.paragraphs[0]
    pb1.text = "Monetization Streams"
    pb1.font.size = Pt(20)
    pb1.font.bold = True
    pb1.font.color.rgb = C_CYAN
    pb2 = tf_b1.add_paragraph()
    pb2.text = "\n• 0.05% Protocol Take-Rate: Settled contract volume ($250M ARR at 1% market penetration).\n• Surety Underwriting API: Verification fees paid by commercial surety bond providers.\n• Zero Crypto Gas: Relayer eliminates balance friction for enterprise bidders."
    pb2.font.size = Pt(14)
    pb2.font.color.rgb = C_WHITE

    add_card(s6, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.8), bg_color=RGBColor(12, 28, 48), border_color=C_PURPLE)
    tf_b2 = s6.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(4.9), Inches(4.2)).text_frame
    tf_b2.word_wrap = True
    pb3 = tf_b2.paragraphs[0]
    pb3.text = "Network Effects & Moat"
    pb3.font.size = Pt(20)
    pb3.font.bold = True
    pb3.font.color.rgb = C_PURPLE
    pb4 = tf_b2.add_paragraph()
    pb4.text = "\n• Municipal Flywheel: Each city onboarded locks regional contractors into the BidTrace relayer.\n• Relayer Sticky Moat: Enterprise API contracts ensure sustainable long-term cash flow.\n• Standards Lock-In: Becomes the mandatory OCDS 1.1 compliance referee."
    pb4.font.size = Pt(14)
    pb4.font.color.rgb = C_WHITE

    s6.notes_slide.notes_text_frame.text = (
        "[SLIDE 6 | 1:35 - 1:50 | 39 Words on Slide]\n"
        "\"Why will this keep working? We monetize through a 0.05% take-rate on awarded contracts plus surety underwriting fees. "
        "Our moat is distribution: contractors pay zero crypto gas, and each onboarded government locks hundreds of contractors "
        "into our verification rail, creating an irreversible compliance standard.\""
    )

    # =========================================================================
    # SLIDE 7: TEAM (Founder-Market Fit & Credentials, <40 words)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)

    th7 = s7.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf7 = th7.text_frame
    p = tf7.paragraphs[0]
    p.text = "FOUNDER-PROBLEM FIT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = tf7.add_paragraph()
    p2.text = "Built for Sovereign Cryptographic Settlement"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    team_cards = [
        ("Solana Anchor Systems", "High-Throughput State Machines", "Temporal slot phase locks, blinded commitments, and on-chain Olympic scoring algorithms.", C_CYAN),
        ("OCDS 1.1 Cryptography", "World Bank Data Standard", "Deterministic RFC 8785 canonical hashing and open-contracting data schemas.", C_PURPLE),
        ("B2G & TradFi Relayers", "Zero-Friction Enterprise", "Zero-gas relayer and air-gapped cryptographic bidder receipts giving contractors legal standing.", C_EMERALD)
    ]
    for i, (title, sub, body, accent) in enumerate(team_cards):
        cx = Inches(1.0 + i * 3.85)
        add_card(s7, cx, Inches(1.9), Inches(3.6), Inches(3.8))
        tb = s7.shapes.add_textbox(cx + Inches(0.2), Inches(2.1), Inches(3.2), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_MUTED
        p3 = tf.add_paragraph()
        p3.text = "\n" + body
        p3.font.size = Pt(13)
        p3.font.color.rgb = C_WHITE

    # Bottom Submission Card
    add_card(s7, Inches(1.0), Inches(5.95), Inches(11.33), Inches(1.15), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tfc = s7.shapes.add_textbox(Inches(1.2), Inches(6.05), Inches(10.9), Inches(0.95)).text_frame
    tfc.word_wrap = True
    pc1 = tfc.paragraphs[0]
    pc1.text = "COLOSSEUM CRYPTO WORLD'S FAIR 2026 SUBMISSION"
    pc1.font.size = Pt(13)
    pc1.font.bold = True
    pc1.font.color.rgb = C_CYAN
    pc2 = tfc.add_paragraph()
    pc2.text = "Live Protocol: bidtrace.net  |  Program ID: x3iSm5BCoXvEfNwT6m6Vs7ApBJtKjvuTm7qKBJtESjZ  |  GitHub: Ujjwal1396/BidTrace"
    pc2.font.size = Pt(12)
    pc2.font.color.rgb = C_WHITE

    s7.notes_slide.notes_text_frame.text = (
        "[SLIDE 7 | 1:50 - 2:00 | 39 Words on Slide]\n"
        "\"We are uniquely built for this problem—combining deep expertise in Solana Anchor engineering, "
        "World Bank OCDS standards, and institutional compliance. "
        "We give contractors independent cryptographic receipts that hold up in legal tribunals. "
        "We built BidTrace to make public infrastructure incorruptible. Thank you.\""
    )

    out_file = "BidTrace_Pitch_Deck_2Min.pptx"
    prs.save(out_file)
    prs.save("public/" + out_file)
    print(f"Updated deck saved to {out_file} and public/{out_file}!")

if __name__ == "__main__":
    create_deck()
