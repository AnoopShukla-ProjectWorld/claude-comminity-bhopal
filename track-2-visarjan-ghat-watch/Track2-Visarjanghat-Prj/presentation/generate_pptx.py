import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    c_dark_navy = RGBColor(15, 23, 42)      # #0F172A
    c_cream = RGBColor(250, 247, 242)        # #FAF7F2
    c_emerald = RGBColor(4, 120, 87)         # #047857
    c_emerald_light = RGBColor(16, 185, 129) # #10B981
    c_amber = RGBColor(217, 119, 6)          # #D97706
    c_rose = RGBColor(225, 29, 72)           # #E11D48
    c_white = RGBColor(255, 255, 255)
    c_stone_text = RGBColor(51, 65, 85)
    c_subtle = RGBColor(100, 116, 139)

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="BHOPAL IMPACT LAB 2026 · TRACK 2", dark=False):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = c_emerald if dark else c_emerald
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = c_white if dark else c_dark_navy

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, c_dark_navy)

    # Accent pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.8), Inches(0.5))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(6, 78, 59)
    pill.line.fill.background()
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "BHOPAL IMPACT LAB 2026 · TRACK 2: VISARJAN GHAT WATCH"
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = c_emerald_light

    # Main Title Box
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(3.0))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = 0
    p_t = tf1.paragraphs[0]
    p_t.text = "Visarjan Ghat Watch\n(विसर्जन घाट वॉच)"
    p_t.font.size = Pt(44)
    p_t.font.bold = True
    p_t.font.color.rgb = c_white

    p_sub = tf1.add_paragraph()
    p_sub.text = "Turning 3 Years of Buried MPPCB Water Tests into an Auditable Action Plan for Bhopal 2026"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Author Card
    author_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.0))
    author_box.fill.solid()
    author_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    author_box.line.color.rgb = RGBColor(51, 65, 85)
    tf_auth = author_box.text_frame
    tf_auth.word_wrap = True
    p_a1 = tf_auth.paragraphs[0]
    p_a1.text = "Team: NeerRakshak   |   Lead: Anoop Shukla (anoopshuklanew00@gmail.com)"
    p_a1.font.size = Pt(14)
    p_a1.font.bold = True
    p_a1.font.color.rgb = c_white
    p_a2 = tf_auth.add_paragraph()
    p_a2.text = "Target Decision: BMC Resource Allocation for Durga Visarjan (20 October 2026 — 9 Days Remaining)"
    p_a2.font.size = Pt(12)
    p_a2.font.color.rgb = c_emerald_light

    # ==========================================
    # SLIDE 2: Problem Statement & Ground Reality
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, c_cream)
    add_header(s2, "The Crisis Behind Bhopal's Immersion Ghats")

    # 4 Cards Layout
    cards_data = [
        ("4 Anoxic Events (0.0 mg/l DO)", "Dissolved Oxygen hit 0 mg/l four times at Bairagarh Kund across 2023-2025. Water at zero oxygen supports no fish life.", c_rose),
        ("89.3% Organic BOD Failure", "100 of 112 Biochemical Oxygen Demand readings exceed statutory limits (<= 3.0 mg/l). Median BOD is 6.4 mg/l (Peak: 22.0 mg/l).", c_amber),
        ("36.2% Oxygen Depletion", "42 of 116 Dissolved Oxygen tests fail CPCB Class B outdoor bathing criteria (>= 5.0 mg/l), creating acute ecological dead-zones.", c_rose),
        ("9 Days to Durga Visarjan", "NGT has banned immersion in Upper/Lower lakes. On 20 Oct 2026, BMC officers must allocate aeration, skimmers & bunds without guesswork.", c_emerald)
    ]

    for idx, (head, desc, col) in enumerate(cards_data):
        left = Inches(0.8 + (idx * 2.95))
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(2.8), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = RGBColor(226, 232, 240)
        
        top_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(2.2), Inches(2.8), Inches(0.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_top = Inches(0.4)
        tf_c.margin_left = tf_c.margin_right = Inches(0.2)
        
        p_ch = tf_c.paragraphs[0]
        p_ch.text = head
        p_ch.font.size = Pt(16)
        p_ch.font.bold = True
        p_ch.font.color.rgb = c_dark_navy

        p_cd = tf_c.add_paragraph()
        p_cd.text = desc
        p_cd.font.size = Pt(13)
        p_cd.font.color.rgb = c_stone_text

    # ==========================================
    # SLIDE 3: The Solution (Visarjan Ghat Watch)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, c_cream)
    add_header(s3, "Visarjan Ghat Watch: Evidence-Based Decision Support")

    sol_items = [
        ("1. Multi-Criteria Risk Scoring (MCDA)", "Combines DO deficit, BOD organic spike, and pH deviation into a normalized 0-100 composite risk score, ranking all 7 ghats from Critical to Controlled."),
        ("2. Real-Time Sensitivity Sliders", "Enables administrative officers to drag weight sliders (DO, BOD, pH) to simulate changing environmental priorities and re-rank ghats in 0.1 seconds."),
        ("3. 100% Traceability & Auditability", "Every test links directly to its source annual MPPCB PDF report and exact page number, ensuring decisions are legally defensible in court/NGT."),
        ("4. Dynamic Ingestion & New Kund Onboarding", "Field inspectors can upload batch multi-parameter Excel/CSV sheets or onboard newly constructed containment kunds with instant automatic re-ranking.")
    ]

    for idx, (title, desc) in enumerate(sol_items):
        top = Inches(2.0 + (idx * 1.25))
        c_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = c_white
        c_box.line.color.rgb = RGBColor(226, 232, 240)
        
        tf_s = c_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = Inches(0.3)
        tf_s.margin_top = Inches(0.15)

        p_st = tf_s.paragraphs[0]
        p_st.text = title
        p_st.font.size = Pt(15)
        p_st.font.bold = True
        p_st.font.color.rgb = c_emerald

        p_sd = tf_s.add_paragraph()
        p_sd.text = desc
        p_sd.font.size = Pt(12)
        p_sd.font.color.rgb = c_stone_text

    # ==========================================
    # SLIDE 4: Architecture & Technology Stack
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, c_dark_navy)
    add_header(s4, "System Architecture & Production Tech Stack", dark=True)

    tech_boxes = [
        ("Backend Core", "Python 3.10+\nFlask Web Server\nSQLite Zero-Config DB\nREST API Endpoints", Inches(0.8)),
        ("Analytics Engine", "Pandas & NumPy\nMCDA Risk Calculator\nCPCB Class B Rules\nAutomated YoY Deltas", Inches(3.8)),
        ("Frontend & GIS", "TailwindCSS & Jinja2\nChart.js Trends\nLeaflet.js GIS Map\nBilingual Switcher", Inches(6.8)),
        ("Zero-Config DevOps", "Windows 1-Click Launcher\nrun.bat automated venv\n7-Step Self Diagnostics\ntest_system.py suite", Inches(9.8))
    ]

    for title, desc, left in tech_boxes:
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(2.7), Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(30, 41, 59)
        box.line.color.rgb = RGBColor(51, 65, 85)

        tf_t = box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = Inches(0.2)
        tf_t.margin_top = Inches(0.4)

        p_th = tf_t.paragraphs[0]
        p_th.text = title
        p_th.font.size = Pt(18)
        p_th.font.bold = True
        p_th.font.color.rgb = c_emerald_light

        p_td = tf_t.add_paragraph()
        p_td.text = desc
        p_td.font.size = Pt(14)
        p_td.font.color.rgb = RGBColor(226, 232, 240)

    # ==========================================
    # SLIDE 5: Priority Rankings of Bhopal's 7 Sites
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, c_cream)
    add_header(s5, "Bhopal Ghat Priority Ranking & Scientific Findings")

    ranking_data = [
        ("#1", "Bairagarh (Sant Hirdaram) kund", "69.7", "CRITICAL", "DO hit 0.0 mg/l 4 times; 100% BOD violations; stagnant mineralized kund.", c_rose),
        ("#2", "Shahpura lake ghat", "26.6", "HIGH", "100% BOD violations (18/18 tests); DO fell to 2.5 mg/l in Durga 2025.", c_amber),
        ("#3", "Malikhedi kund", "23.5", "HIGH", "Post-immersion organic surge (BOD jumped 1.6 -> 16.8 mg/l in 2023).", c_amber),
        ("#4", "Rani Kamlapati / Kamla Park", "20.0", "HIGH", "Chronically polluted Lower Lake; DO stayed at ~2.5 mg/l in Durga 2025.", c_amber),
        ("#5", "Hathaikheda dam / kund", "19.1", "MODERATE", "Extreme BOD surge (22.0 mg/l); alkaline pH 8.92; dam reservoir.", RGBColor(79, 70, 229)),
        ("#6", "Khatlapura ghat", "17.0", "MODERATE", "Baseline Lower Lake pollution; metal & conductivity spike in Ganesh 2024.", RGBColor(79, 70, 229)),
        ("#7", "Prempura ghat", "6.3", "LOW", "Consistently the cleanest natural lake ghat; lowest median BOD (3.2 mg/l).", c_emerald)
    ]

    for idx, (rank, name, score, level, note, col) in enumerate(ranking_data):
        top = Inches(1.8 + (idx * 0.75))
        r_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.65))
        r_box.fill.solid()
        r_box.fill.fore_color.rgb = c_white
        r_box.line.color.rgb = RGBColor(226, 232, 240)

        tf_r = r_box.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = Inches(0.2)
        tf_r.margin_top = Inches(0.1)

        p_r = tf_r.paragraphs[0]
        p_r.text = f"{rank}  {name}   [Score: {score} | {level}] — {note}"
        p_r.font.size = Pt(11)
        p_r.font.bold = True
        p_r.font.color.rgb = col

    # ==========================================
    # SLIDE 6: Dynamic Ingestion & Live Re-ranking
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, c_cream)
    add_header(s6, "100% Dynamic Architecture: Ingestion to Instant Re-ranking")

    dyn_cards = [
        ("Multi-Parameter Bulk Ingestion", "Upload batch CSV or Excel sheets (.xlsx) covering all 13 parameters in a single file. Supports Long and Wide formats with smart context overrides.", Inches(0.8)),
        ("Dynamic Ghat Onboarding", "Register newly constructed artificial kunds with GPS coordinates. The system automatically creates a dedicated deep-dive trends page with default banners.", Inches(4.8)),
        ("Instant Recalculation", "Every newly entered sample or uploaded sheet automatically triggers the MCDA engine, recalculates scores, and re-sorts priority rankings in < 1 second.", Inches(8.8))
    ]

    for title, desc, left in dyn_cards:
        d_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(3.7), Inches(4.5))
        d_box.fill.solid()
        d_box.fill.fore_color.rgb = c_white
        d_box.line.color.rgb = RGBColor(226, 232, 240)

        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = Inches(0.3)
        tf_d.margin_top = Inches(0.4)

        p_dh = tf_d.paragraphs[0]
        p_dh.text = title
        p_dh.font.size = Pt(16)
        p_dh.font.bold = True
        p_dh.font.color.rgb = c_emerald

        p_dd = tf_d.add_paragraph()
        p_dd.text = desc
        p_dd.font.size = Pt(13)
        p_dd.font.color.rgb = c_stone_text

    # ==========================================
    # SLIDE 7: Unique Selling Propositions (USPs)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, c_cream)
    add_header(s7, "Core Innovations & Unique Selling Propositions")

    usps = [
        ("1. Judicial Auditability (100% Traceability)", "No black-box hallucinations. Clicking any test reading opens the official MPPCB annual technical report at the exact page number, ready for court scrutiny."),
        ("2. Interactive Administrative Agency", "Municipal engineers are not locked into static outputs; dynamic sliders empower real-time adjustment of DO, BOD, and pH priorities."),
        ("3. Bilingual Decision Memo", "A forwardable bilingual executive memo formatted for WhatsApp/Email sharing or 1-click administrative printing for senior decision-makers."),
        ("4. Grounded Conversational AI", "A context-grounded bilingual assistant answering complex queries strictly from MPPCB records with phonetic Hinglish matching.")
    ]

    for idx, (head, text) in enumerate(usps):
        top = Inches(2.0 + (idx * 1.25))
        u_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        u_box.fill.solid()
        u_box.fill.fore_color.rgb = c_white
        u_box.line.color.rgb = RGBColor(226, 232, 240)

        tf_u = u_box.text_frame
        tf_u.word_wrap = True
        tf_u.margin_left = Inches(0.3)
        tf_u.margin_top = Inches(0.15)

        p_uh = tf_u.paragraphs[0]
        p_uh.text = head
        p_uh.font.size = Pt(15)
        p_uh.font.bold = True
        p_uh.font.color.rgb = c_dark_navy

        p_ud = tf_u.add_paragraph()
        p_ud.text = text
        p_ud.font.size = Pt(12)
        p_ud.font.color.rgb = c_stone_text

    # ==========================================
    # SLIDE 8: 3-Minute Live Demo Flow
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, c_cream)
    add_header(s8, "Structured 3-Minute Live Demonstration Flow")

    demo_steps = [
        ("Step 1: The Problem (0:00 - 0:45)", "Launch localhost:5000 via run.bat. Highlight the 4 KPI cards: 4 zero DO readings at Bairagarh and 89.3% statewide BOD organic pollution."),
        ("Step 2: Dynamic Sliders (0:45 - 1:15)", "Drag DO slider from 50% to 70%. Show how rankings and Chart.js bar chart re-order live in 0.1 seconds based on MCDA calculations."),
        ("Step 3: Deep-Dive & Traceability (1:15 - 2:00)", "Open 'View Trends' on Bairagarh. Filter historical readings by year/festival. Click 'Page 28 PDF' to open the original scanned MPPCB document."),
        ("Step 4: Dynamic Bulk Ingestion (2:00 - 2:30)", "Open 'Import Water Quality Data' modal. Upload multi-parameter spreadsheet and demonstrate automated ranking recalculation."),
        ("Step 5: Bilingual AI Assistant (2:30 - 3:00)", "Ask chatbot: 'bairagadh ka pani kaisa hai?' Show instant grounded response with verified MPPCB citations.")
    ]

    for idx, (title, desc) in enumerate(demo_steps):
        top = Inches(2.0 + (idx * 1.0))
        d_step = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.88))
        d_step.fill.solid()
        d_step.fill.fore_color.rgb = c_white
        d_step.line.color.rgb = RGBColor(226, 232, 240)

        tf_dm = d_step.text_frame
        tf_dm.word_wrap = True
        tf_dm.margin_left = Inches(0.25)
        tf_dm.margin_top = Inches(0.1)

        p_dmt = tf_dm.paragraphs[0]
        p_dmt.text = title
        p_dmt.font.size = Pt(13)
        p_dmt.font.bold = True
        p_dmt.font.color.rgb = c_emerald

        p_dmd = tf_dm.add_paragraph()
        p_dmd.text = desc
        p_dmd.font.size = Pt(11)
        p_dmd.font.color.rgb = c_stone_text

    # ==========================================
    # SLIDE 9: Conclusion & Team Closing
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, c_dark_navy)
    add_header(s9, "Empowering Bhopal's Water Heritage", dark=True)

    c_box9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.5))
    c_box9.fill.solid()
    c_box9.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_box9.line.color.rgb = RGBColor(51, 65, 85)

    tf_c9 = c_box9.text_frame
    tf_c9.word_wrap = True
    tf_c9.margin_left = tf_c9.margin_right = Inches(0.5)
    tf_c9.margin_top = Inches(0.5)

    p_c9_1 = tf_c9.paragraphs[0]
    p_c9_1.text = "Operational Ready for 20 October 2026 Durga Visarjan"
    p_c9_1.font.size = Pt(24)
    p_c9_1.font.bold = True
    p_c9_1.font.color.rgb = c_emerald_light

    p_c9_2 = tf_c9.add_paragraph()
    p_c9_2.text = "\n• 100% Open Source: Offered to Government of Madhya Pradesh & MPSeDC.\n• Zero API Dependencies: Operates entirely locally with high reliability.\n• Extensible Blueprint: Architecture ready for 100+ immersion sites across MP.\n\nTeam NeerRakshak: Anoop Shukla (anoopshuklanew00@gmail.com)\nGitHub: https://github.com/AnoopShukla-ProjectWorld/claude-community-bhopal"
    p_c9_2.font.size = Pt(15)
    p_c9_2.font.color.rgb = RGBColor(226, 232, 240)

    out_path = os.path.join("presentation", "NeerRakshak_Visarjan_Ghat_Watch.pptx")
    prs.save(out_path)
    print(f"[SUCCESS] Presentation saved to {out_path}")

if __name__ == '__main__':
    create_presentation()
