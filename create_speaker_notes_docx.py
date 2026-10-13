import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_speaker_notes_docx():
    doc = Document()

    # Set page margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("BidTrace: Master Speaker Notes & Cue Sheet")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(10, 37, 64)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Official 2-Minute Executive Pitch Script — Word-for-Word Pacing Guide")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Executive Metadata Box (Table)
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    headers = [
        ("TOTAL DURATION", "120s (1:55 + 5s buffer)"),
        ("TOTAL WORDS", "275 Words"),
        ("PACING", "135–140 words/min"),
        ("REHEARSAL APP", "bidtrace.net/pitch-deck.html")
    ]

    for col_idx, (label, val) in enumerate(headers):
        # Header row
        cell_top = meta_table.cell(0, col_idx)
        set_cell_background(cell_top, "0F172A")
        p = cell_top.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(label)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(56, 189, 248)

        # Value row
        cell_bot = meta_table.cell(1, col_idx)
        set_cell_background(cell_bot, "F1F5F9")
        p2 = cell_bot.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(4)
        r2 = p2.add_run(val)
        r2.font.name = "Calibri"
        r2.font.size = Pt(10)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 7 Slides Data
    slides_data = [
        {
            "num": "Slide 1",
            "title": "Cover Slide",
            "time": "0:00 – 0:06 (6 seconds)",
            "words": "14 Words",
            "on_screen": "BidTrace Logo | \"Goodbye Bid Rigging.\" | $13T Sovereign Spend | 400ms Clock | Zero Crypto Gas",
            "script": "“Good morning, I’m [Your Name]. This is BidTrace: Goodbye Bid Rigging.”",
            "cues": "Make direct eye contact with judges. Pause for 1 full second after “Goodbye Bid Rigging” so the hook lands clearly before advancing."
        },
        {
            "num": "Slide 2",
            "title": "The Problem",
            "time": "0:06 – 0:28 (22 seconds)",
            "words": "48 Words",
            "on_screen": "The $2.5 Trillion Corruption Tax | Centralized SQL Exploit Window (Diagram) | Forensic Authority Badge",
            "script": "“Public procurement is a $13 Trillion market, but 25%—over $2.5 Trillion—is lost to corruption.\n\nAs a lawyer who handled NPAs and bad loan recoveries at a commercial bank, I’ve seen this wreckage firsthand: backdated bids, leaked prices, and rigged tenders disguised as legitimate processes on centralized SQL databases.”",
            "cues": "Deliver “NPAs and bad loan recoveries at a commercial bank” with personal gravity. This immediately anchors your unassailable domain expertise."
        },
        {
            "num": "Slide 3",
            "title": "Solution (BidTrace)",
            "time": "0:28 – 1:00 (32 seconds)",
            "words": "72 Words",
            "on_screen": "“The Cryptographic Swiss Vault” | 4-Row Vulnerability ➔ Cryptographic Proof Table | Zero-Fiat Relayer Banner",
            "script": "“BidTrace is the cryptographic Swiss Vault for public procurement. We replace database admin trust with mathematical certainty:\n\nContractors encrypt bids in-browser with AES-256 dual envelopes—servers never see plaintext.\n\nDeadlines are locked to Solana’s Proof of History clock—late bids are rejected at the bytecode level.\n\nAnd proposals are scored blindly, discarding rogue outlier bribes.\n\nBest of all, our zero-fiat relayer requires zero crypto tokens, making BidTrace 100% legally compliant worldwide.”",
            "cues": "Step rhythmically through the 3 technical countermeasures. Emphasize “zero crypto tokens... 100% legally compliant worldwide” to disarm regulatory skepticism."
        },
        {
            "num": "Slide 4",
            "title": "Market Opportunity & Institutional Validation",
            "time": "1:00 – 1:20 (20 seconds)",
            "words": "46 Words",
            "on_screen": "SOM ($120B Beachhead) | SAM ($2.5T) | TAM ($13.0T) | World Bank Jan 2021 Report Box",
            "script": "“Our beachhead is the $120 Billion in multilateral projects funded by the World Bank and ADB.\n\nIn its landmark report on disruptive procurement, the World Bank validated blockchain's anti-corruption power, but flagged privacy, gas costs, and token bans. BidTrace was purpose-built to solve all three.”",
            "cues": "Cite the World Bank report with total authority—you are presenting the exact solution to the World Bank's published roadmap."
        },
        {
            "num": "Slide 5",
            "title": "Business Model & Monetization",
            "time": "1:20 – 1:38 (18 seconds)",
            "words": "40 Words",
            "on_screen": "Enterprise GovTech SaaS ($50k–$250k) | 0.05% Volume Integrity Fee | 189-Country Cascade | 200x ROI Bar",
            "script": "“We charge an annual enterprise SaaS license from $50k to $250k, plus a 0.05% integrity fee funded directly through existing contractor submission fee budgets.\n\nWhen multilateral lenders mandate BidTrace on loan tranches, it cascades across 189 member countries automatically.”",
            "cues": "Deliver smoothly. Highlight that fees fit directly into existing public budget lines without requiring new legislation."
        },
        {
            "num": "Slide 6",
            "title": "Team / Why Me?",
            "time": "1:38 – 1:55 (17 seconds)",
            "words": "40 Words",
            "on_screen": "Tri-Force: Commercial Lawyer + Banking NPA Veteran + Cryptographic Architect | Live Devnet Badges",
            "script": "“I built BidTrace because I sit at the exact intersection of law, banking forensics, and cryptography.\n\nI didn’t read about tender fraud in a textbook—I saw the defaults on my desk.\n\nThe prototype is live. Join us. Goodbye Bid Rigging.”",
            "cues": "Deliver “I saw the defaults on my desk” with quiet, unshakeable conviction. This is your emotional climax before closing on the brand hook."
        },
        {
            "num": "Slide 7",
            "title": "Join the Cause & Live Demo",
            "time": "1:55 – 2:00 (5 seconds)",
            "words": "15 Words",
            "on_screen": "BidTrace Logo | bidtrace.net | @bidtrace | Active Demo Links",
            "script": "“If you like our cause, visit us on bidtrace.net and join us on X. Thank you.”",
            "cues": "Smile, invite judges to visit the live interactive demo at bidtrace.net, and welcome the applause."
        }
    ]

    for s in slides_data:
        # Slide Header Container Table
        card_table = doc.add_table(rows=4, cols=1)
        card_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        card_table.autofit = False

        # Row 0: Slide Title & Window Header
        c0 = card_table.cell(0, 0)
        set_cell_background(c0, "0F172A")
        set_cell_margins(c0, top=120, bottom=120, left=180, right=180)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r_num = p0.add_run(f"{s['num'].upper()} — {s['title'].upper()}")
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(11)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(255, 255, 255)

        r_time = p0.add_run(f"    [{s['time']}  |  {s['words']}]")
        r_time.font.name = "Calibri"
        r_time.font.size = Pt(9.5)
        r_time.font.bold = True
        r_time.font.color.rgb = RGBColor(56, 189, 248)

        # Row 1: On-Screen Visual Context
        c1 = card_table.cell(1, 0)
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c1, top=100, bottom=100, left=180, right=180)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r_vis_lbl = p1.add_run("ON SCREEN VISUAL: ")
        r_vis_lbl.font.name = "Calibri"
        r_vis_lbl.font.size = Pt(9)
        r_vis_lbl.font.bold = True
        r_vis_lbl.font.color.rgb = RGBColor(100, 116, 139)

        r_vis_txt = p1.add_run(s['on_screen'])
        r_vis_txt.font.name = "Calibri"
        r_vis_txt.font.size = Pt(9.5)
        r_vis_txt.font.color.rgb = RGBColor(51, 65, 85)

        # Row 2: Spoken Script (Large, Distinct Block)
        c2 = card_table.cell(2, 0)
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c2, top=140, bottom=140, left=200, right=200)
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(4)
        p2.paragraph_format.line_spacing = 1.25

        r_script_lbl = p2.add_run("WORD-FOR-WORD SPOKEN SCRIPT:\n")
        r_script_lbl.font.name = "Calibri"
        r_script_lbl.font.size = Pt(9)
        r_script_lbl.font.bold = True
        r_script_lbl.font.color.rgb = RGBColor(14, 165, 233)

        r_script = p2.add_run(s['script'])
        r_script.font.name = "Calibri"
        r_script.font.size = Pt(12)
        r_script.font.bold = True
        r_script.font.color.rgb = RGBColor(15, 23, 42)

        # Row 3: Stage Direction & Cues
        c3 = card_table.cell(3, 0)
        set_cell_background(c3, "F1F5F9")
        set_cell_margins(c3, top=100, bottom=100, left=180, right=180)
        p3 = c3.paragraphs[0]
        p3.paragraph_format.space_before = Pt(2)
        p3.paragraph_format.space_after = Pt(2)
        r_cue_lbl = p3.add_run("STAGE DIRECTION / VOCAL CUE: ")
        r_cue_lbl.font.name = "Calibri"
        r_cue_lbl.font.size = Pt(9)
        r_cue_lbl.font.bold = True
        r_cue_lbl.font.color.rgb = RGBColor(180, 83, 9)

        r_cue_txt = p3.add_run(s['cues'])
        r_cue_txt.font.name = "Calibri"
        r_cue_txt.font.size = Pt(9.5)
        r_cue_txt.font.italic = True
        r_cue_txt.font.color.rgb = RGBColor(71, 85, 105)

        # Spacing between slides
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(8)

    # Rehearsal Summary Table
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(10)
    p_sum.paragraph_format.space_after = Pt(4)
    r_sum_title = p_sum.add_run("Executive Timing & Rehearsal Summary")
    r_sum_title.font.name = "Calibri"
    r_sum_title.font.size = Pt(14)
    r_sum_title.font.bold = True
    r_sum_title.font.color.rgb = RGBColor(10, 37, 64)

    sum_table = doc.add_table(rows=8, cols=4)
    sum_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    sum_headers = ["SLIDE", "TARGET TIME", "WORD COUNT", "CORE MILESTONE"]
    for i, h in enumerate(sum_headers):
        cell = sum_table.cell(0, i)
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    sum_rows = [
        ("Slide 1: Cover", "0:00 – 0:06", "14", "Opening hook landed"),
        ("Slide 2: Problem", "0:06 – 0:28", "48", "Banking & NPA credential established"),
        ("Slide 3: Solution", "0:28 – 1:00", "72", "4 cryptographic proofs + global legal compliance"),
        ("Slide 4: Market", "1:00 – 1:20", "46", "World Bank 2021 report validation cited"),
        ("Slide 5: Business Model", "1:20 – 1:38", "40", "Enterprise SaaS + 189-country cascade"),
        ("Slide 6: Team / Why Me", "1:38 – 1:55", "40", "“Saw defaults on my desk” emotional climax"),
        ("Slide 7: CTA", "1:55 – 2:00", "15", "bidtrace.net & @bidtrace on screen")
    ]

    for row_idx, data in enumerate(sum_rows):
        bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, val in enumerate(data):
            cell = sum_table.cell(row_idx + 1, col_idx)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            if col_idx in [1, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(71, 85, 105)

    out_docx = "BidTrace_Speaker_Notes_2Min.docx"
    doc.save(out_docx)
    doc.save("public/" + out_docx)
    print(f"Successfully generated {out_docx} and public/{out_docx}!")

if __name__ == "__main__":
    create_speaker_notes_docx()
