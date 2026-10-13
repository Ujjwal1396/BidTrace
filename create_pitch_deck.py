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
    C_BG = RGBColor(7, 11, 22)           # Deep Midnight (#070b16)
    C_CARD = RGBColor(12, 19, 38)        # Card Background (#0c1326)
    C_CARD_BORDER = RGBColor(28, 40, 72) # Subtle Border (#1c2848)
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
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(1.2), Inches(1.4), width=Inches(1.8))

    # Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), Inches(1.45), Inches(4.8), Inches(0.42))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(16, 32, 55)
    b1.line.color.rgb = C_CYAN
    b1.text_frame.text = "SOVEREIGN PUBLIC PROCUREMENT PROTOCOL"
    b1.text_frame.paragraphs[0].font.size = Pt(11)
    b1.text_frame.paragraphs[0].font.bold = True
    b1.text_frame.paragraphs[0].font.color.rgb = C_CYAN
    b1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Brand Title
    tb_title = s1.shapes.add_textbox(Inches(3.2), Inches(1.95), Inches(9.0), Inches(1.2))
    p = tb_title.text_frame.paragraphs[0]
    p.text = "BidTrace"
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Big Winning Headline
    tb_h = s1.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(11.0), Inches(1.5))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "Goodbye Bid Rigging."
    p_h.font.size = Pt(38)
    p_h.font.bold = True
    p_h.font.color.rgb = C_CYAN
    p_sub = tf_h.add_paragraph()
    p_sub.text = "Cryptographic sealed bidding for public infrastructure contracts."
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = C_TEXT_MUTED

    # 3 Stat Cards
    stats_s1 = [
        ("$13.0 Trillion", "Annual Sovereign Spend (15-20% GDP)", C_CYAN),
        ("400ms Clock", "Proof of History Precision Deadline Lock", C_PURPLE),
        ("Zero Crypto Gas", "100% Legally Compliant Worldwide", C_EMERALD)
    ]
    for i, (num, lbl, col) in enumerate(stats_s1):
        bx = Inches(1.2 + i * 3.75)
        add_card(s1, bx, Inches(5.1), Inches(3.5), Inches(1.6))
        tb_st = s1.shapes.add_textbox(bx + Inches(0.2), Inches(5.25), Inches(3.1), Inches(1.3))
        tf_st = tb_st.text_frame
        p_n = tf_st.paragraphs[0]
        p_n.text = num
        p_n.font.size = Pt(26)
        p_n.font.bold = True
        p_n.font.color.rgb = col
        p_l = tf_st.add_paragraph()
        p_l.text = lbl
        p_l.font.size = Pt(12)
        p_l.font.color.rgb = C_TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "[SLIDE 1 | 0:00 - 0:06 | 14 Words]\n"
        "\"Good morning, I’m [Your Name]. This is BidTrace: Goodbye Bid Rigging.\""
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)

    th2 = s2.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.3), Inches(1.1))
    tf2 = th2.text_frame
    p = tf2.paragraphs[0]
    p.text = "THE PROBLEM"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p2 = tf2.add_paragraph()
    p2.text = "The $2.5 Trillion Corruption Tax on Public Procurement"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # Left: The Global Hemorrhage & Personal Credibility
    add_card(s2, Inches(1.0), Inches(1.85), Inches(5.4), Inches(4.9), bg_color=C_CARD, border_color=RGBColor(80, 20, 35))
    tfl = s2.shapes.add_textbox(Inches(1.3), Inches(2.05), Inches(4.8), Inches(4.4)).text_frame
    tfl.word_wrap = True
    pl1 = tfl.paragraphs[0]
    pl1.text = "$2.5 Trillion Lost"
    pl1.font.size = Pt(34)
    pl1.font.bold = True
    pl1.font.color.rgb = C_ROSE
    pl2 = tfl.add_paragraph()
    pl2.text = "20% to 25% of Global Public Infrastructure Spend\n(World Bank & UN Estimates)"
    pl2.font.size = Pt(14)
    pl2.font.bold = True
    pl2.font.color.rgb = C_WHITE
    pl3 = tfl.add_paragraph()
    pl3.text = "\n⚖️ FORENSIC AUTHORITY:\nAs a lawyer who worked on bad loan recoveries and NPAs at a commercial bank, I've seen this wreckage firsthand: defaulted contracts, fraudulent bank guarantees, and rigged tender processes."
    pl3.font.size = Pt(13)
    pl3.font.color.rgb = C_AMBER

    # Right: Centralized SQL Exploit Window
    add_card(s2, Inches(6.8), Inches(1.85), Inches(5.5), Inches(4.9), bg_color=RGBColor(12, 24, 44), border_color=C_CYAN)
    tfr = s2.shapes.add_textbox(Inches(7.1), Inches(2.05), Inches(4.9), Inches(4.4)).text_frame
    tfr.word_wrap = True
    pr1 = tfr.paragraphs[0]
    pr1.text = "Centralized SQL Trust"
    pr1.font.size = Pt(28)
    pr1.font.bold = True
    pr1.font.color.rgb = C_CYAN
    pr2 = tfr.add_paragraph()
    pr2.text = "Legacy Systems (SAP Ariba, Procore, Govt Portals)"
    pr2.font.size = Pt(14)
    pr2.font.bold = True
    pr2.font.color.rgb = C_WHITE
    pr3 = tfr.add_paragraph()
    pr3.text = (
        "\n• Pre-Deadline Leaks: Admins peek at sealed prices before cutoff.\n\n"
        "• SQL Backdating: Late bids accepted with a simple UPDATE command:\n"
        "   UPDATE bids SET submitted_at = '14:49:00';\n\n"
        "• Exposed Trade Secrets: Losing bidders' proprietary unit prices leaked to competitors."
    )
    pr3.font.size = Pt(13)
    pr3.font.color.rgb = C_TEXT_MUTED

    s2.notes_slide.notes_text_frame.text = (
        "[SLIDE 2 | 0:06 - 0:28 | 48 Words]\n"
        "\"Public procurement is a $13 Trillion market, but 25%—over $2.5 Trillion—is lost to corruption. "
        "As a lawyer who handled NPAs and bad loan recoveries at a commercial bank, I’ve seen this wreckage firsthand: "
        "backdated bids, leaked prices, and rigged tenders disguised as legitimate processes on centralized SQL databases.\""
    )

    # =========================================================================
    # SLIDE 3: SOLUTION (The Cryptographic Swiss Vault)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)

    th3 = s3.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.3), Inches(1.1))
    tf3 = th3.text_frame
    p = tf3.paragraphs[0]
    p.text = "SOLUTION: BIDTRACE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p2 = tf3.add_paragraph()
    p2.text = "“The Cryptographic Swiss Vault for Public Procurement”"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    sol_rows = [
        ("1. Pre-Deadline Leaks", "Client-Side AES-256 Dual Envelopes", "Encrypted in browser; zero plaintext on servers until official reveal.", C_CYAN),
        ("2. Backdated Late Bids", "Solana Proof of History Clock", "Bytecode deadline lock; mathematically impossible to backdate (0x1773).", C_PURPLE),
        ("3. Evaluator Bribery", "Blinded Olympic Scoring", "Anonymized review by vetted pool; automatically discards rogue score spikes.", C_EMERALD),
        ("4. Trade Secret Theft", "On-Chain Commercial Secrecy Lock", "Disqualified bidders' financial bids remain cryptographically locked forever (0x1778).", C_AMBER)
    ]
    for i, (crime, weapon, detail, accent) in enumerate(sol_rows):
        cy = Inches(1.85 + i * 1.15)
        add_card(s3, Inches(1.0), cy, Inches(11.33), Inches(1.05))
        tb = s3.shapes.add_textbox(Inches(1.2), cy + Inches(0.1), Inches(10.9), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{crime}  ➔  {weapon}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = detail
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_WHITE

    # Bottom note
    add_card(s3, Inches(1.0), Inches(6.55), Inches(11.33), Inches(0.55), bg_color=RGBColor(16, 32, 55), border_color=C_CYAN)
    tb_b = s3.shapes.add_textbox(Inches(1.2), Inches(6.6), Inches(10.9), Inches(0.45))
    tb_b.text_frame.text = "⚡ Zero-Fiat Gas Relayer: Standard browser keys — zero tokens required ➔ 100% legally compliant worldwide."
    tb_b.text_frame.paragraphs[0].font.size = Pt(12)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = C_CYAN

    s3.notes_slide.notes_text_frame.text = (
        "[SLIDE 3 | 0:28 - 1:00 | 72 Words]\n"
        "\"BidTrace is the cryptographic Swiss Vault for public procurement. "
        "We replace database admin trust with mathematical certainty: "
        "Contractors encrypt bids in-browser with AES-256 dual envelopes—servers never see plaintext. "
        "Deadlines are locked to Solana’s Proof of History clock—late bids are rejected at the bytecode level. "
        "And proposals are scored blindly, discarding rogue outlier bribes. "
        "Best of all, our zero-fiat relayer requires zero crypto tokens, making BidTrace 100% legally compliant worldwide.\""
    )

    # =========================================================================
    # SLIDE 4: MARKET OPPORTUNITY & WORLD BANK VALIDATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)

    th4 = s4.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.3), Inches(1.1))
    tf4 = th4.text_frame
    p = tf4.paragraphs[0]
    p.text = "MARKET OPPORTUNITY & INSTITUTIONAL VALIDATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p2 = tf4.add_paragraph()
    p2.text = "A $13 Trillion Market Demanding Cryptographic Truth"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    # Left: Sizing
    add_card(s4, Inches(1.0), Inches(1.85), Inches(5.4), Inches(4.9))
    tf_m = s4.shapes.add_textbox(Inches(1.3), Inches(2.05), Inches(4.8), Inches(4.4)).text_frame
    tf_m.word_wrap = True
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Market Sizing"
    pm1.font.size = Pt(20)
    pm1.font.bold = True
    pm1.font.color.rgb = C_CYAN
    pm2 = tf_m.add_paragraph()
    pm2.text = (
        "\n• SOM: $120 Billion Beachhead\n"
        "  Multilateral Development Bank Projects (World Bank, ADB)\n"
        "  Mandated to enforce OCDS 1.1 anti-corruption transparency.\n\n"
        "• SAM: $2.5 Trillion\n"
        "  High-risk infrastructure tenders where bid rigging concentrates.\n\n"
        "• TAM: $13.0 Trillion\n"
        "  Total annual global public procurement (~15-20% World GDP)."
    )
    pm2.font.size = Pt(13)
    pm2.font.color.rgb = C_WHITE

    # Right: World Bank Report 2021
    add_card(s4, Inches(6.8), Inches(1.85), Inches(5.5), Inches(4.9), bg_color=RGBColor(12, 24, 44), border_color=C_CYAN)
    tf_wb = s4.shapes.add_textbox(Inches(7.1), Inches(2.05), Inches(4.9), Inches(4.4)).text_frame
    tf_wb.word_wrap = True
    pw1 = tf_wb.paragraphs[0]
    pw1.text = "World Bank Landmark Report"
    pw1.font.size = Pt(20)
    pw1.font.bold = True
    pw1.font.color.rgb = C_CYAN
    pw2 = tf_wb.add_paragraph()
    pw2.text = "\"Disruptive Technologies in Public Procurement\" (Jan 2021)"
    pw2.font.size = Pt(13)
    pw2.font.bold = True
    pw2.font.color.rgb = C_WHITE
    pw3 = tf_wb.add_paragraph()
    pw3.text = (
        "\nExplicitly validated blockchain's anti-corruption power, but cited 3 key hurdles:\n\n"
        "1. Commercial Privacy Risk ➔ BidTrace AES-256 Dual Envelopes\n"
        "2. Gas Fee Volatility ➔ Solana $0.00025 sub-second txs\n"
        "3. Crypto Legal Restrictions ➔ Zero-Fiat Gas Relayer\n\n"
        "✓ BidTrace is purpose-built to answer the World Bank's roadmap."
    )
    pw3.font.size = Pt(12)
    pw3.font.color.rgb = C_TEXT_MUTED

    s4.notes_slide.notes_text_frame.text = (
        "[SLIDE 4 | 1:00 - 1:20 | 46 Words]\n"
        "\"Our beachhead is the $120 Billion in multilateral projects funded by the World Bank and ADB. "
        "In its landmark report on disruptive procurement, the World Bank validated blockchain's anti-corruption power, "
        "but flagged privacy, gas costs, and token bans. BidTrace was purpose-built to solve all three.\""
    )

    # =========================================================================
    # SLIDE 5: BUSINESS MODEL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)

    th5 = s5.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.3), Inches(1.1))
    tf5 = th5.text_frame
    p = tf5.paragraphs[0]
    p.text = "BUSINESS MODEL & MONETIZATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p2 = tf5.add_paragraph()
    p2.text = "High-Margin GovTech SaaS with 200x Anti-Corruption ROI"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    biz_streams = [
        ("Enterprise GovTech SaaS", "$50k – $250k / Year", "Annual license for ministries, public utilities & large EPC developers. Turnkey e-GP integration.", C_CYAN),
        ("Per-Tender Integrity Fee", "0.05% of Tender Value", "Funded directly from existing contractor submission fees charged on every tender.", C_PURPLE),
        ("Institutional Cascade", "189 Member Countries", "When World Bank or ADB mandates BidTrace on loan tranches, adoption cascades with zero CAC.", C_EMERALD)
    ]
    for i, (title, sub, body, accent) in enumerate(biz_streams):
        bx = Inches(1.0 + i * 3.85)
        add_card(s5, bx, Inches(1.85), Inches(3.6), Inches(3.7))
        tb = s5.shapes.add_textbox(bx + Inches(0.2), Inches(2.05), Inches(3.2), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tf.add_paragraph()
        p3.text = "\n" + body
        p3.font.size = Pt(13)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom ROI Bar
    add_card(s5, Inches(1.0), Inches(5.8), Inches(11.33), Inches(1.1), bg_color=RGBColor(12, 28, 48), border_color=C_EMERALD)
    tf_roi = s5.shapes.add_textbox(Inches(1.2), Inches(5.95), Inches(10.9), Inches(0.8)).text_frame
    tf_roi.word_wrap = True
    proi1 = tf_roi.paragraphs[0]
    proi1.text = "THE CUSTOMER MATH: 200x RETURN ON INVESTMENT"
    proi1.font.size = Pt(14)
    proi1.font.bold = True
    proi1.font.color.rgb = C_EMERALD
    proi2 = tf_roi.add_paragraph()
    proi2.text = "Eliminates a 20%–25% corruption loss for a <0.1% platform cost. Fits directly into existing public budget lines."
    proi2.font.size = Pt(13)
    proi2.font.color.rgb = C_WHITE

    s5.notes_slide.notes_text_frame.text = (
        "[SLIDE 5 | 1:20 - 1:38 | 40 Words]\n"
        "\"We charge an annual enterprise SaaS license from $50k to $250k, plus a 0.05% integrity fee "
        "funded directly through existing contractor submission fee budgets. "
        "When multilateral lenders mandate BidTrace on loan tranches, it cascades across 189 member countries automatically.\""
    )

    # =========================================================================
    # SLIDE 6: TEAM / WHY ME?
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)

    th6 = s6.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.3), Inches(1.1))
    tf6 = th6.text_frame
    p = tf6.paragraphs[0]
    p.text = "TEAM / WHY ME?"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = tf6.add_paragraph()
    p2.text = "Law + Banking NPA Forensics + Cryptography"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    team_cards = [
        ("Commercial Lawyer", "Legal & Regulatory", "Deep expertise in Public Procurement Acts, FIDIC contracts, and tender dispute arbitration.", C_AMBER),
        ("Commercial Bank NPA", "Forensic Recovery", "Investigated bad loans, defaulted contractor bank guarantees (MT760), and fraudulent tenders up close.", C_CYAN),
        ("Cryptographic Systems", "Engineering Architecture", "Built the full-stack BidTrace protocol on Solana: Anchor smart contracts, OCDS 1.1, and gas relayer.", C_PURPLE)
    ]
    for i, (title, sub, body, accent) in enumerate(team_cards):
        cx = Inches(1.0 + i * 3.85)
        add_card(s6, cx, Inches(1.85), Inches(3.6), Inches(3.6))
        tb = s6.shapes.add_textbox(cx + Inches(0.2), Inches(2.05), Inches(3.2), Inches(3.2))
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
        p3.font.size = Pt(13)
        p3.font.color.rgb = C_WHITE

    # Live Prototype Status
    add_card(s6, Inches(1.0), Inches(5.7), Inches(11.33), Inches(1.2), bg_color=RGBColor(12, 28, 48), border_color=C_CYAN)
    tf_live = s6.shapes.add_textbox(Inches(1.2), Inches(5.85), Inches(10.9), Inches(0.9)).text_frame
    tf_live.word_wrap = True
    pl1 = tf_live.paragraphs[0]
    pl1.text = "LIVE PROTOCOL EXECUTION STATUS"
    pl1.font.size = Pt(13)
    pl1.font.bold = True
    pl1.font.color.rgb = C_CYAN
    pl2 = tf_live.add_paragraph()
    pl2.text = "10 Anchor Instructions on Devnet  |  78/78 Passing Unit Tests  |  Live 1-Click Attack Simulator"
    pl2.font.size = Pt(13)
    pl2.font.color.rgb = C_WHITE

    s6.notes_slide.notes_text_frame.text = (
        "[SLIDE 6 | 1:38 - 1:55 | 40 Words]\n"
        "\"I built BidTrace because I sit at the exact intersection of law, banking forensics, and cryptography. "
        "I didn’t read about tender fraud in a textbook—I saw the defaults on my desk. "
        "The prototype is live. Join us. Goodbye Bid Rigging.\""
    )

    # =========================================================================
    # SLIDE 7: CALL TO ACTION (Website, X, and Closing)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)

    if os.path.exists(logo_path):
        s7.shapes.add_picture(logo_path, Inches(5.8), Inches(1.2), width=Inches(1.7))

    tb_end = s7.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(11.33), Inches(1.4))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True
    pe1 = tf_end.paragraphs[0]
    pe1.text = "BidTrace"
    pe1.font.size = Pt(50)
    pe1.font.bold = True
    pe1.font.color.rgb = C_WHITE
    pe1.alignment = PP_ALIGN.CENTER
    pe2 = tf_end.add_paragraph()
    pe2.text = "\"Goodbye Bid Rigging.\""
    pe2.font.size = Pt(28)
    pe2.font.bold = True
    pe2.font.color.rgb = C_CYAN
    pe2.alignment = PP_ALIGN.CENTER

    # Connect Cards (Web & X)
    add_card(s7, Inches(2.2), Inches(4.7), Inches(4.2), Inches(1.7), bg_color=C_CARD, border_color=C_CYAN)
    tfc1 = s7.shapes.add_textbox(Inches(2.4), Inches(4.9), Inches(3.8), Inches(1.3)).text_frame
    pc1 = tfc1.paragraphs[0]
    pc1.text = "🌐  bidtrace.net"
    pc1.font.size = Pt(24)
    pc1.font.bold = True
    pc1.font.color.rgb = C_CYAN
    pc2 = tfc1.add_paragraph()
    pc2.text = "Live Interactive Protocol Portals & Attack Demos"
    pc2.font.size = Pt(12)
    pc2.font.color.rgb = C_TEXT_MUTED

    add_card(s7, Inches(6.9), Inches(4.7), Inches(4.2), Inches(1.7), bg_color=C_CARD, border_color=C_PURPLE)
    tfc2 = s7.shapes.add_textbox(Inches(7.1), Inches(4.9), Inches(3.8), Inches(1.3)).text_frame
    pc3 = tfc2.paragraphs[0]
    pc3.text = "𝕏   @bidtrace"
    pc3.font.size = Pt(24)
    pc3.font.bold = True
    pc3.font.color.rgb = C_PURPLE
    pc4 = tfc2.add_paragraph()
    pc4.text = "Follow Technical Releases & Community Updates"
    pc4.font.size = Pt(12)
    pc4.font.color.rgb = C_TEXT_MUTED

    s7.notes_slide.notes_text_frame.text = (
        "[SLIDE 7 | 1:55 - 2:00 | 15 Words]\n"
        "\"If you like our cause, visit us on bidtrace.net and join us on X. Thank you.\""
    )

    out_file = "BidTrace_Pitch_Deck_2Min.pptx"
    prs.save(out_file)
    prs.save("public/" + out_file)
    print(f"Updated 7-slide deck successfully saved to {out_file} and public/{out_file}!")

if __name__ == "__main__":
    create_deck()
