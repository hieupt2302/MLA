import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==================== COLOR PALETTE ====================
BG_COLOR = RGBColor(248, 250, 252)       # #F8FAFC
NAVY = RGBColor(15, 23, 42)              # #0F172A
NAVY_CARD = RGBColor(26, 37, 57)         # #1A2539
NAVY_LIGHT = RGBColor(30, 41, 59)        # #1E293B
BLUE = RGBColor(37, 99, 235)             # #2563EB
BLUE_MUTED = RGBColor(59, 130, 246)      # #3B82F6
BLUE_CIRCLE_1 = RGBColor(22, 38, 70)     # Dark concentric
BLUE_CIRCLE_2 = RGBColor(33, 73, 155)    # Medium concentric
BLUE_CIRCLE_3 = RGBColor(37, 99, 235)    # Light concentric
CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF
CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0
GRAY_TEXT = RGBColor(100, 116, 139)      # #64748B
GRAY_MUTED = RGBColor(148, 163, 184)     # #94A3B8
GRAY_LINE = RGBColor(203, 213, 225)      # #CBD5E1
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(22, 163, 74)            # #16A34A
ORANGE = RGBColor(217, 119, 6)           # #D97706
RED = RGBColor(220, 38, 38)              # #DC2626
LIGHT_RED_BG = RGBColor(254, 242, 242)   # #FEF2F2

FONT_HEADING = "Trebuchet MS"
FONT_BODY = "Calibri"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_top_bar(slide, tag_left, page_num):
        # Top tag
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(8), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = "— "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = BLUE
        r2 = p.add_run()
        r2.text = tag_left.upper()
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = BLUE

        # Page num
        tb_page = slide.shapes.add_textbox(Inches(11.8), Inches(0.4), Inches(0.9), Inches(0.35))
        tf_p = tb_page.text_frame
        tf_p.word_wrap = False
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]
        pp.alignment = PP_ALIGN.RIGHT
        rp = pp.add_run()
        rp.text = f"{page_num}  /  09"
        rp.font.name = FONT_BODY
        rp.font.size = Pt(9)
        rp.font.bold = True
        rp.font.color.rgb = GRAY_TEXT

    def add_footer(slide, left_text, right_text):
        tb_left = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(8.5), Inches(0.3))
        tf_l = tb_left.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        r_l = p_l.add_run()
        r_l.text = left_text.upper()
        r_l.font.name = FONT_BODY
        r_l.font.size = Pt(8)
        r_l.font.color.rgb = GRAY_MUTED

        if right_text:
            tb_right = slide.shapes.add_textbox(Inches(9.2), Inches(7.05), Inches(3.5), Inches(0.3))
            tf_r = tb_right.text_frame
            tf_r.word_wrap = False
            tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
            p_r = tf_r.paragraphs[0]
            p_r.alignment = PP_ALIGN.RIGHT
            r_r = p_r.add_run()
            r_r.text = right_text.upper()
            r_r.font.name = FONT_BODY
            r_r.font.size = Pt(8)
            r_r.font.color.rgb = GRAY_MUTED

    def add_title(slide, text_segments, top=0.75):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(top), Inches(11.5), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        for text, color, bold, size in text_segments:
            run = p.add_run()
            run.text = text
            run.font.name = FONT_HEADING
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
        return tb

    def add_card(slide, left, top, width, height, fill_color=CARD_BG, border_color=CARD_BORDER, border_width=1):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(border_width)
        else:
            shape.line.fill.background()
        return shape

    def add_notes(slide, notes):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Right concentric target circles
    # Center at (12.5, 3.75)
    circle_center_x = 12.5
    circle_center_y = 3.5
    radii = [6.5, 4.8, 3.4, 2.0]
    colors = [
        (None, RGBColor(226, 232, 240)), 
        (BLUE_CIRCLE_1, None),
        (BLUE_CIRCLE_2, None),
        (BLUE_CIRCLE_3, None)
    ]
    for r, (fill, border) in zip(radii, colors):
        c = slide1.shapes.add_shape(MSO_SHAPE.OVAL, 
                                    Inches(circle_center_x - r), 
                                    Inches(circle_center_y - r), 
                                    Inches(r * 2), Inches(r * 2))
        if fill:
            c.fill.solid()
            c.fill.fore_color.rgb = fill
        else:
            c.fill.background()
        if border:
            c.line.color.rgb = border
            c.line.width = Pt(1.5)
        else:
            c.line.fill.background()

    # White box in center
    sq = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(circle_center_x - 0.5), Inches(circle_center_y - 0.5), Inches(1), Inches(1))
    sq.fill.solid()
    sq.fill.fore_color.rgb = WHITE
    sq.line.fill.background()

    # Top tag
    tb_tag = slide1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(6), Inches(0.5))
    tf = tb_tag.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "|   62FIT4MLA — MIDTERM"
    r.font.name = FONT_BODY
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = BLUE

    # Big 3-line Title
    tb_title = slide1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.5), Inches(3.2))
    tf = tb_title.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    lines = [
        ("Discourse", NAVY),
        ("Effectiveness", BLUE),
        ("Prediction", NAVY)
    ]
    for i, (txt, clr) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = txt
        run.font.name = FONT_HEADING
        run.font.size = Pt(56)
        run.font.bold = True
        run.font.color.rgb = clr
        p.space_after = Pt(2)

    # Subtitle
    tb_sub = slide1.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(7.5), Inches(1.0))
    tf = tb_sub.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Supporting teachers in evaluating argument quality in argumentative essays."
    run.font.name = FONT_BODY
    run.font.size = Pt(15)
    run.font.color.rgb = NAVY

    # Group Card
    add_card(slide1, 0.8, 5.7, 2.5, 0.9, CARD_BG, CARD_BORDER)
    tb_grp = slide1.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(2.2), Inches(0.6))
    tf = tb_grp.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Group 06"
    run.font.name = FONT_HEADING
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = NAVY

    add_footer(slide1, "Slide — 01 / 09", "Machine Learning Applications · Fall 2026\nGroup project · Midterm presentation")
    add_notes(slide1, "Welcome to our midterm presentation. We are addressing Discourse Effectiveness Prediction to support teachers evaluating student argumentative essays.")

    # =========================================================================
    # SLIDE 2: Problem, User & Pipeline
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_top_bar(slide2, "01 / PROBLEM & USER", "02")
    add_title(slide2, [
        ("How can ML surface what a ", NAVY, True, 28),
        ("teacher", BLUE, True, 28),
        ("\nshould read first?", BLUE, True, 28)
    ], top=0.7)

    # Subtitle section
    tb = slide2.shapes.add_textbox(Inches(0.6), Inches(2.05), Inches(5), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "— SUGGESTED PIPELINE — 5 STAGES"
    r.font.name = FONT_BODY
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT

    # Pipeline connecting line
    line = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.0), Inches(12.1), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE_MUTED
    line.line.fill.background()

    # 5 pipeline cards
    steps = [
        ("STEP 01", "Complete\nessay", "Raw submission, full text.", False),
        ("STEP 02", "Pre-identified\ncomponents", "Claim, Evidence, Rebuttal...", False),
        ("STEP 03", "Classification\nmodel", "3-class score per component.", True),
        ("STEP 04", "Prediction\n+ confidence", "Label per span.", False),
        ("STEP 05", "Teacher\nreview", "Accept / modify / reject.", False),
    ]
    card_w = 2.25
    gap = 0.22
    for i, (tag, title, desc, is_dark) in enumerate(steps):
        cx = 0.6 + i * (card_w + gap)
        bg_col = NAVY_CARD if is_dark else CARD_BG
        brd_col = None if is_dark else CARD_BORDER
        add_card(slide2, cx, 2.35, card_w, 1.8, bg_col, brd_col)

        tb = slide2.shapes.add_textbox(Inches(cx + 0.15), Inches(2.45), Inches(card_w - 0.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = tag
        r1.font.name = FONT_BODY
        r1.font.size = Pt(8)
        r1.font.bold = True
        r1.font.color.rgb = BLUE if not is_dark else BLUE_MUTED
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = title
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(13)
        r2.font.bold = True
        r2.font.color.rgb = WHITE if is_dark else NAVY
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        r3 = p3.add_run()
        r3.text = desc
        r3.font.name = FONT_BODY
        r3.font.size = Pt(9)
        r3.font.color.rgb = GRAY_MUTED if is_dark else GRAY_TEXT

    # 3 Summary Cards
    # Card 1: User
    add_card(slide2, 0.6, 4.35, 3.8, 1.25, CARD_BG, CARD_BORDER)
    tb = slide2.shapes.add_textbox(Inches(0.75), Inches(4.45), Inches(3.5), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "USER\n"
    r.font.name = FONT_BODY
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "English writing "
    r2.font.size = Pt(12)
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "teacher"
    r3.font.size = Pt(12)
    r3.font.bold = True
    r3.font.color.rgb = NAVY
    r4 = p.add_run()
    r4.text = ", grades 6–12, accountable for class-wide assessment."
    r4.font.size = Pt(12)
    r4.font.color.rgb = NAVY

    # Card 2: Per Essay
    add_card(slide2, 4.65, 4.35, 3.8, 1.25, CARD_BG, CARD_BORDER)
    tb = slide2.shapes.add_textbox(Inches(4.8), Inches(4.45), Inches(3.5), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "PER ESSAY\n"
    r.font.name = FONT_BODY
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "8–14 "
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(28)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = " discourse components each"
    r3.font.name = FONT_BODY
    r3.font.size = Pt(11)
    r3.font.color.rgb = GRAY_TEXT

    # Card 3: Per Batch (Dark)
    add_card(slide2, 8.7, 4.35, 4.0, 1.25, NAVY_CARD, None)
    tb = slide2.shapes.add_textbox(Inches(8.85), Inches(4.45), Inches(3.7), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "PER BATCH\n"
    r.font.name = FONT_BODY
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_MUTED
    r2 = p.add_run()
    r2.text = "~385 "
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(28)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    r3 = p.add_run()
    r3.text = " components to review"
    r3.font.name = FONT_BODY
    r3.font.size = Pt(11)
    r3.font.color.rgb = GRAY_MUTED

    # Bottom Callout Bar
    bar_line = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.8), Inches(0.04), Inches(0.7))
    bar_line.fill.solid()
    bar_line.fill.fore_color.rgb = BLUE
    bar_line.line.fill.background()

    tb_call = slide2.shapes.add_textbox(Inches(0.75), Inches(5.8), Inches(11.5), Inches(0.7))
    tf = tb_call.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "DECISION SUPPORTED\n"
    r.font.name = FONT_BODY
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = BLUE
    r2 = p.add_run()
    r2.text = "Which discourse components are likely "
    r2.font.name = FONT_BODY
    r2.font.size = Pt(12)
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "weak"
    r3.font.name = FONT_BODY
    r3.font.size = Pt(12)
    r3.font.bold = True
    r3.font.color.rgb = NAVY
    r4 = p.add_run()
    r4.text = " and deserve the teacher's immediate attention?"
    r4.font.name = FONT_BODY
    r4.font.size = Pt(12)
    r4.font.color.rgb = NAVY

    add_footer(slide2, "Criterion — 01 Problem Formulation (20 marks)", "MVP · Gold Segmentation")
    add_notes(slide2, "An English writing teacher must evaluate discourse quality in argumentative essays. 8-14 components per essay x 35 students = ~385 components per batch. The goal is to surface weak components first.")

    # =========================================================================
    # SLIDE 3: Dataset & Data Challenges
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_top_bar(slide3, "02 / DATASET & CHALLENGES", "03")
    add_title(slide3, [
        ("PERSUADE 2.0 — large, public, and\n", NAVY, True, 28),
        ("severely imbalanced.", BLUE, True, 28)
    ], top=0.7)

    # 4 Top Stats Cards
    stats = [
        ("ESSAYS", "25,995", "Train 15,593 · Test 10,402", CARD_BG, CARD_BORDER, NAVY, GRAY_TEXT),
        ("DISCOURSE ELEMENTS", "285,383", "Labeled 237,966", NAVY_CARD, None, WHITE, GRAY_MUTED),
        ("LICENSE", "CC BY 4.0", "Public — both splits in hand", CARD_BG, CARD_BORDER, GREEN, GRAY_TEXT),
        ("WRITERS · PROMPTS", "US, 6–12", "15 argumentative prompts", CARD_BG, CARD_BORDER, NAVY, GRAY_TEXT)
    ]
    sw = 2.85
    for i, (tag, val, sub, bg, brd, vclr, sclr) in enumerate(stats):
        sx = 0.6 + i * (sw + 0.22)
        add_card(slide3, sx, 1.9, sw, 1.25, bg, brd)
        tb = slide3.shapes.add_textbox(Inches(sx + 0.15), Inches(1.98), Inches(sw - 0.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = FONT_BODY
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = GRAY_MUTED if bg == NAVY_CARD else GRAY_TEXT
        r2 = p.add_run()
        r2.text = val + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(24)
        r2.font.bold = True
        r2.font.color.rgb = vclr
        r3 = p.add_run()
        r3.text = sub
        r3.font.name = FONT_BODY
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = sclr

    # Left Section: Corpus Source & Key Fields
    add_card(slide3, 0.6, 3.35, 5.2, 2.0, CARD_BG, CARD_BORDER)
    tb = slide3.shapes.add_textbox(Inches(0.8), Inches(3.45), Inches(4.8), Inches(1.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "CORPUS SOURCE\n"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "Crossley et al. (2024), Assessing Writing\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "Public repository on GitHub. 27 columns of metadata, targets, and demographic fields. Public Kaggle / Learning Agency Lab mirror, ready for both training and held-out testing.\n"
    r3.font.size = Pt(9)
    r3.font.color.rgb = GRAY_TEXT
    r4 = p.add_run()
    r4.text = "github.com / scrosseye / persuade_corpus_2.0"
    r4.font.size = Pt(9)
    r4.font.color.rgb = BLUE

    # Badges for fields
    fields = [
        ("discourse_text", False), ("full_text", False), ("discourse_type", False), ("prompt_name", False),
        ("discourse_effectiveness ~ target", True), ("holistic_essay_score", False), ("essay_word_count", False)
    ]
    tb = slide3.shapes.add_textbox(Inches(0.6), Inches(5.45), Inches(5.2), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "KEY FIELDS (SELECTED FROM 27 COLUMNS)"
    r.font.size = Pt(7.5)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT

    bx = 0.6
    by = 5.75
    for fld, is_tgt in fields:
        fw = len(fld) * 0.08 + 0.3
        if bx + fw > 5.8:
            bx = 0.6
            by += 0.38
        add_card(slide3, bx, by, fw, 0.3, NAVY_CARD if is_tgt else CARD_BG, None if is_tgt else CARD_BORDER)
        tb_f = slide3.shapes.add_textbox(Inches(bx), Inches(by + 0.04), Inches(fw), Inches(0.24))
        p = tb_f.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.margin_left = p.margin_top = p.margin_right = p.margin_bottom = 0
        r = p.add_run()
        r.text = fld
        r.font.size = Pt(8)
        r.font.bold = is_tgt
        r.font.color.rgb = WHITE if is_tgt else NAVY
        bx += fw + 0.1

    # Right Section: Label Distribution Card
    add_card(slide3, 6.1, 3.35, 6.6, 3.4, CARD_BG, CARD_BORDER)
    tb = slide3.shapes.add_textbox(Inches(6.3), Inches(3.45), Inches(6.2), Inches(0.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "CRITICAL CHALLENGE — LABEL DISTRIBUTION\n"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "Most rare class is what teachers need most"
    r2.font.size = Pt(8.5)
    r2.font.bold = True
    r2.font.color.rgb = RED

    # Progress bar (Adequate 79.3%, Effective 16.3%, Ineffective 4.4%)
    bar_y = 4.1
    b1 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.3), Inches(bar_y), Inches(4.8), Inches(0.35))
    b1.fill.solid()
    b1.fill.fore_color.rgb = NAVY_LIGHT
    b1.line.fill.background()
    p = b1.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "ADEQUATE · 79.3%"
    r.font.size = Pt(8)
    r.font.color.rgb = WHITE

    b2 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.1), Inches(bar_y), Inches(1.0), Inches(0.35))
    b2.fill.solid()
    b2.fill.fore_color.rgb = GREEN
    b2.line.fill.background()
    p = b2.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "16.3%"
    r.font.size = Pt(8)
    r.font.color.rgb = WHITE

    b3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.1), Inches(bar_y), Inches(0.4), Inches(0.35))
    b3.fill.solid()
    b3.fill.fore_color.rgb = RED
    b3.line.fill.background()

    # 3 Detail Cards below bar
    dc_w = 1.95
    # Adequate
    add_card(slide3, 6.3, 4.65, dc_w, 1.15, CARD_BG, CARD_BORDER)
    tb = slide3.shapes.add_textbox(Inches(6.4), Inches(4.75), Inches(dc_w - 0.2), Inches(1.0))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "ADEQUATE\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "188,607\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(17)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "majority class — trivial to predict"
    r3.font.size = Pt(7.5)
    r3.font.color.rgb = GRAY_TEXT

    # Effective
    add_card(slide3, 8.4, 4.65, dc_w, 1.15, CARD_BG, CARD_BORDER)
    tb = slide3.shapes.add_textbox(Inches(8.5), Inches(4.75), Inches(dc_w - 0.2), Inches(1.0))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "EFFECTIVE\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "38,672\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(17)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "16.3% of total"
    r3.font.size = Pt(7.5)
    r3.font.color.rgb = GRAY_TEXT

    # Ineffective (Highlight)
    add_card(slide3, 10.5, 4.65, dc_w + 0.15, 1.15, LIGHT_RED_BG, RED, border_width=1.5)
    tb = slide3.shapes.add_textbox(Inches(10.6), Inches(4.75), Inches(dc_w - 0.05), Inches(1.0))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "INEFFECTIVE\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = RED
    r2 = p.add_run()
    r2.text = "10,687\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(17)
    r2.font.bold = True
    r2.font.color.rgb = RED
    r3 = p.add_run()
    r3.text = "← teachers need this most"
    r3.font.size = Pt(7.5)
    r3.font.color.rgb = RED

    # 3 Strategy tags
    tb_strat = slide3.shapes.add_textbox(Inches(6.3), Inches(6.05), Inches(6.3), Inches(0.5))
    tf = tb_strat.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    strats = [("01", " Class weights & focal loss     "), ("02", " Stratified per-fold sampling     "), ("03", " Per-class recall focus")]
    for num, txt in strats:
        r1 = p.add_run()
        r1.text = num
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = BLUE
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = NAVY

    # Bottom note
    add_card(slide3, 0.6, 6.75, 0.03, 0.25, RED, None)
    tb = slide3.shapes.add_textbox(Inches(0.7), Inches(6.7), Inches(10.0), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "Accuracy alone is misleading. "
    r.font.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RED
    r2 = p.add_run()
    r2.text = "Always predicting 'Adequate' → 79.3% accuracy, 0% recall on Ineffective."
    r2.font.size = Pt(8)
    r2.font.color.rgb = NAVY

    add_footer(slide3, "Dataset Reference: Crossley et al. (2024)", "")
    add_notes(slide3, "PERSUADE 2.0 dataset has 25,995 essays and 285,383 elements. The critical challenge is the label imbalance: Ineffective is only 4.5%, yet it is the most critical for teachers.")

    # =========================================================================
    # SLIDE 4: Related Work & Design Rationale
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_top_bar(slide4, "03 / RELATED WORK & DESIGN RATIONALE", "04")
    add_title(slide4, [
        ("Prior work shaped three honest constraints — we\nbuild ", NAVY, True, 26),
        ("in their shadow", BLUE, True, 26),
        (", not against them.", NAVY, True, 26)
    ], top=0.7)

    # 3 Paper Cards
    papers = [
        ("PAPER · 01", "Ding, Bexte & Horbach", "(2023) — Score It All Together",
         "Logistic regression baseline QWK 0.41 rises to 0.50 with context + type + prompt.",
         "Gold boundaries only; 157 long essays truncated; English only.",
         "https://doi.org/10.18653/v1/2023.findings-acl.825", BLUE),
        ("PAPER · 02", "Favero et al.", "(2026) — Small LLMs for Argument Mining",
         "7B–9B LLMs tested; fine-tuning helps structure but not quality.",
         "Recall on Ineffective: only 29.78%; needs A100 GPU.",
         "https://ceur-ws.org/Vol-4166/", GREEN),
        ("PAPER · 03", "Baffour, Saxberg & Crossley", "(2023) — Analyzing Bias",
         "Effectiveness prediction shows moderate bias by ELL, race, and economic status.",
         "Aggregate metrics hide subgroup gaps; scope limited to competition winners.",
         "https://doi.org/10.18653/v1/2023.bea-1.21", ORANGE),
    ]
    pw = 3.85
    for i, (tag, authors, title_p, finding, lim, link, accent_clr) in enumerate(papers):
        px = 0.6 + i * (pw + 0.25)
        # Card body
        add_card(slide4, px, 1.85, pw, 2.5, CARD_BG, CARD_BORDER)
        # Top accent bar
        acc = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(px), Inches(1.85), Inches(pw), Inches(0.04))
        acc.fill.solid()
        acc.fill.fore_color.rgb = accent_clr
        acc.line.fill.background()

        tb = slide4.shapes.add_textbox(Inches(px + 0.15), Inches(1.95), Inches(pw - 0.3), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = accent_clr

        r2 = p.add_run()
        r2.text = authors + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(13)
        r2.font.bold = True
        r2.font.color.rgb = NAVY

        r3 = p.add_run()
        r3.text = title_p + "\n\n"
        r3.font.size = Pt(8.5)
        r3.font.italic = True
        r3.font.color.rgb = GRAY_TEXT

        r4 = p.add_run()
        r4.text = "KEY FINDING\n"
        r4.font.size = Pt(7.5)
        r4.font.bold = True
        r4.font.color.rgb = GRAY_TEXT

        r5 = p.add_run()
        r5.text = finding + "\n\n"
        r5.font.size = Pt(8.5)
        r5.font.color.rgb = NAVY

        r6 = p.add_run()
        r6.text = "LIMITATION\n"
        r6.font.size = Pt(7.5)
        r6.font.bold = True
        r6.font.color.rgb = RED if accent_clr != BLUE else ORANGE

        r7 = p.add_run()
        r7.text = lim + "\n\n"
        r7.font.size = Pt(8.5)
        r7.font.color.rgb = GRAY_TEXT

        r8 = p.add_run()
        r8.text = "LINK\n"
        r8.font.size = Pt(7)
        r8.font.bold = True
        r8.font.color.rgb = GRAY_MUTED

        r9 = p.add_run()
        r9.text = link
        r9.font.size = Pt(7.5)
        r9.font.color.rgb = BLUE

    # Bottom Table: Prior Limitations -> Our Design Decisions
    tb = slide4.shapes.add_textbox(Inches(0.6), Inches(4.5), Inches(8), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "— FROM LIMITATIONS → OUR DESIGN DECISIONS"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT

    # Table component
    table_shape = slide4.shapes.add_table(5, 3, Inches(0.6), Inches(4.8), Inches(12.1), Inches(1.9))
    table = table_shape.table
    table.columns[0].width = Inches(5.0)
    table.columns[1].width = Inches(0.5)
    table.columns[2].width = Inches(6.6)

    # Header
    table.cell(0, 0).text = "PRIOR LIMITATION"
    table.cell(0, 1).text = ""
    table.cell(0, 2).text = "OUR DESIGN DECISION"
    for c in [0, 1, 2]:
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_CARD
        for p in cell.text_frame.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.bold = True
                run.font.color.rgb = WHITE

    rows_data = [
        ("All prior work uses gold segmentation", "Honest scope — MVP uses pre-given boundaries"),
        ("LLM recall on Ineffective ≈ 30%", "Don't assume complex = better; compare fairly under same conditions"),
        ("Aggregate metrics hide subgroup bias", "Report per-class AND per-subgroup metrics when sample allows"),
        ("No paper proves classroom benefit", "Frame output as a 'suggestion + confidence', teacher accepts/rejects"),
    ]
    for r_idx, (lim_t, dec_t) in enumerate(rows_data):
        row = r_idx + 1
        table.cell(row, 0).text = lim_t
        table.cell(row, 1).text = "→"
        table.cell(row, 2).text = dec_t
        bg_r = CARD_BG if row % 2 == 1 else RGBColor(241, 245, 249)
        for c in [0, 1, 2]:
            cell = table.cell(row, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_r
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = NAVY if c != 1 else BLUE
                    if c == 1: run.font.bold = True

    add_footer(slide4, "Academic References & Design Justification", "")
    add_notes(slide4, "Prior work shaped three constraints: Ding et al. showed LR baseline QWK 0.41->0.50; Favero et al. showed 7B-9B LLMs struggle on Ineffective recall (29.78%); Baffour et al. reported bias across subgroups.")

    # =========================================================================
    # SLIDE 5: Task & Model Plans
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_top_bar(slide5, "04 / TASK & MODEL PLANS", "05")
    add_title(slide5, [
        ("Two classical families, justified — ", NAVY, True, 28),
        ("not 'try\neverything'.", BLUE, True, 28)
    ], top=0.7)

    # Top Pipeline Card (Dark Navy)
    add_card(slide5, 0.6, 1.8, 12.1, 0.8, NAVY_CARD, None)
    tb_pipe = slide5.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(0.7))
    tf = tb_pipe.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "INPUT: "
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = BLUE_MUTED
    p.add_run().text = "discourse_text + context + type + prompt        "
    p.runs[1].font.size = Pt(8.5)
    p.runs[1].font.color.rgb = WHITE

    p.add_run().text = "TASK: "
    p.runs[2].font.bold = True
    p.runs[2].font.size = Pt(8.5)
    p.runs[2].font.color.rgb = BLUE_MUTED
    p.add_run().text = "Multi-class text classification (3 ordinal classes)        "
    p.runs[3].font.size = Pt(8.5)
    p.runs[3].font.color.rgb = WHITE

    p.add_run().text = "OUTPUT: "
    p.runs[4].font.bold = True
    p.runs[4].font.size = Pt(8.5)
    p.runs[4].font.color.rgb = BLUE_MUTED
    p.add_run().text = "Ineffective | Adequate | Effective + confidence score"
    p.runs[5].font.size = Pt(8.5)
    p.runs[5].font.color.rgb = WHITE

    # Plan A Card (White, blue left accent)
    add_card(slide5, 0.6, 2.75, 5.9, 2.8, CARD_BG, CARD_BORDER)
    acc = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(2.75), Inches(0.06), Inches(2.8))
    acc.fill.solid()
    acc.fill.fore_color.rgb = BLUE
    acc.line.fill.background()

    # Watermark 'A'
    tb_wm = slide5.shapes.add_textbox(Inches(5.0), Inches(2.8), Inches(1.4), Inches(1.4))
    p = tb_wm.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "A"
    r.font.name = FONT_HEADING
    r.font.size = Pt(60)
    r.font.bold = True
    r.font.color.rgb = RGBColor(241, 245, 249)

    tb_pa = slide5.shapes.add_textbox(Inches(0.85), Inches(2.85), Inches(5.0), Inches(2.6))
    tf = tb_pa.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "PLAN A — REQUIRED BASELINE\n"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE
    r2 = p.add_run()
    r2.text = "TF-IDF + Logistic Regression\n\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(20)
    r2.font.bold = True
    r2.font.color.rgb = NAVY

    r3 = p.add_run()
    r3.text = "FAMILY                                      IMBALANCE\n"
    r3.font.size = Pt(7.5)
    r3.font.bold = True
    r3.font.color.rgb = GRAY_TEXT
    r4 = p.add_run()
    r4.text = "Generalized linear model             class_weight = 'balanced'\n\n"
    r4.font.size = Pt(8.5)
    r4.font.color.rgb = NAVY

    r5 = p.add_run()
    r5.text = "FEATURES                                EXPECTED QWK\n"
    r5.font.size = Pt(7.5)
    r5.font.bold = True
    r5.font.color.rgb = GRAY_TEXT
    r6 = p.add_run()
    r6.text = "unigrams+bigrams (15K)             "
    r6.font.size = Pt(8.5)
    r6.font.color.rgb = NAVY
    r7 = p.add_run()
    r7.text = "~0.40 – 0.50\n\n"
    r7.font.size = Pt(14)
    r7.font.bold = True
    r7.font.color.rgb = BLUE

    r8 = p.add_run()
    r8.text = "Why this model — fast, interpretable coefficients that teachers can read."
    r8.font.size = Pt(8.5)
    r8.font.color.rgb = GRAY_TEXT

    # Plan B Card (Dark Navy)
    add_card(slide5, 6.8, 2.75, 5.9, 2.8, NAVY_CARD, None)
    acc = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(2.75), Inches(0.06), Inches(2.8))
    acc.fill.solid()
    acc.fill.fore_color.rgb = BLUE_MUTED
    acc.line.fill.background()

    # Watermark 'B'
    tb_wm = slide5.shapes.add_textbox(Inches(11.2), Inches(2.8), Inches(1.4), Inches(1.4))
    p = tb_wm.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "B"
    r.font.name = FONT_HEADING
    r.font.size = Pt(60)
    r.font.bold = True
    r.font.color.rgb = RGBColor(37, 50, 75)

    tb_pb = slide5.shapes.add_textbox(Inches(7.05), Inches(2.85), Inches(5.0), Inches(2.6))
    tf = tb_pb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "PLAN B — REQUIRED 2nd FAMILY\n"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE_MUTED
    r2 = p.add_run()
    r2.text = "TF-IDF + Linear SVM\n\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(20)
    r2.font.bold = True
    r2.font.color.rgb = WHITE

    r3 = p.add_run()
    r3.text = "FAMILY                                      IMBALANCE\n"
    r3.font.size = Pt(7.5)
    r3.font.bold = True
    r3.font.color.rgb = GRAY_MUTED
    r4 = p.add_run()
    r4.text = "Max-margin classifier                 class_weight = 'balanced'\n\n"
    r4.font.size = Pt(8.5)
    r4.font.color.rgb = WHITE

    r5 = p.add_run()
    r5.text = "FEATURES                                EXPECTED QWK\n"
    r5.font.size = Pt(7.5)
    r5.font.bold = True
    r5.font.color.rgb = GRAY_MUTED
    r6 = p.add_run()
    r6.text = "same TF-IDF + one-hot + len      "
    r6.font.size = Pt(8.5)
    r6.font.color.rgb = WHITE
    r7 = p.add_run()
    r7.text = "~0.42 – 0.52\n\n"
    r7.font.size = Pt(14)
    r7.font.bold = True
    r7.font.color.rgb = BLUE_MUTED

    r8 = p.add_run()
    r8.text = "Why this model — stronger margin-based boundary on sparse, high-dim text."
    r8.font.size = Pt(8.5)
    r8.font.color.rgb = GRAY_MUTED

    # Extension Card (Bottom)
    add_card(slide5, 0.6, 5.75, 12.1, 1.0, CARD_BG, CARD_BORDER)
    tb_ext = slide5.shapes.add_textbox(Inches(0.8), Inches(5.85), Inches(9.8), Inches(0.8))
    tf = tb_ext.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "EXTENSION — IF A + B COMPLETE\n"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "Plan C · BERT / DeBERTa  "
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "Captures semantic context TF-IDF misses. Ablation: text only → +context → +type → +prompt."
    r3.font.size = Pt(9)
    r3.font.color.rgb = GRAY_TEXT

    # Optional badge
    add_card(slide5, 11.2, 5.95, 1.2, 0.4, CARD_BG, GREEN)
    tb_opt = slide5.shapes.add_textbox(Inches(11.2), Inches(6.02), Inches(1.2), Inches(0.3))
    p = tb_opt.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "OPTIONAL"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GREEN

    add_footer(slide5, "Criterion — 03 ML Task Alignment + Model Families (25 marks)", "")
    add_notes(slide5, "Two classical model families: Plan A is Logistic Regression (interpretable baseline), Plan B is Linear SVM (max-margin classifier). Plan C is BERT fine-tuning as an extension.")

    # =========================================================================
    # SLIDE 6: Feature Engineering & Ablations
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_top_bar(slide6, "05 / FEATURE ENGINEERING", "06")
    add_title(slide6, [
        ("Three streams, four ablations, ", NAVY, True, 28),
        ("reported honestly.", BLUE, True, 28)
    ], top=0.7)

    # 3 Streams on left
    stream_data = [
        ("STREAM 01", "discourse_text", "TF-IDF · 1–2 grams · max 15K", BLUE),
        ("STREAM 02", "discourse_type", "One-hot encoding, 7 categories", GREEN),
        ("STREAM 03", "Length features", "word / char / sentence counts", ORANGE),
    ]
    for i, (tag, name, desc, clr) in enumerate(stream_data):
        sy = 1.9 + i * 1.05
        add_card(slide6, 0.6, sy, 2.8, 0.9, CARD_BG, CARD_BORDER)
        # Left color marker
        sq = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(sy + 0.15), Inches(0.1), Inches(0.1))
        sq.fill.solid()
        sq.fill.fore_color.rgb = clr
        sq.line.fill.background()

        tb = slide6.shapes.add_textbox(Inches(0.95), Inches(sy + 0.1), Inches(2.3), Inches(0.75))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = tag + "\n"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = clr
        r2 = p.add_run()
        r2.text = name + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = NAVY
        r3 = p.add_run()
        r3.text = desc
        r3.font.size = Pt(7.5)
        r3.font.color.rgb = GRAY_TEXT

    # Feature Matrix Box (Dark Navy)
    add_card(slide6, 4.0, 2.1, 1.9, 1.8, NAVY_CARD, None)
    tb_fm = slide6.shapes.add_textbox(Inches(4.15), Inches(2.25), Inches(1.6), Inches(1.5))
    tf = tb_fm.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "FEATURE MATRIX\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE_MUTED
    r2 = p.add_run()
    r2.text = "Sparse,\nhigh-dim\n\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    r3 = p.add_run()
    r3.text = "n × 15K+ cols"
    r3.font.size = Pt(8)
    r3.font.color.rgb = GRAY_MUTED

    # Model Box
    add_card(slide6, 6.4, 2.35, 1.8, 1.25, CARD_BG, CARD_BORDER)
    tb_m = slide6.shapes.add_textbox(Inches(6.55), Inches(2.45), Inches(1.5), Inches(1.05))
    tf = tb_m.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "MODEL\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "LR or SVM\n"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    r3 = p.add_run()
    r3.text = "class_weight = 'balanced'"
    r3.font.size = Pt(7.5)
    r3.font.color.rgb = GRAY_TEXT

    # Prediction Box (Dark Navy)
    add_card(slide6, 8.6, 2.35, 1.9, 1.25, NAVY_CARD, None)
    tb_pr = slide6.shapes.add_textbox(Inches(8.75), Inches(2.45), Inches(1.6), Inches(1.05))
    tf = tb_pr.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "PREDICTION\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE_MUTED
    r2 = p.add_run()
    r2.text = "3 classes +\nconfidence"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(12)
    r2.font.bold = True
    r2.font.color.rgb = WHITE

    # Teacher Decides Box
    add_card(slide6, 9.6, 3.8, 1.9, 1.0, CARD_BG, CARD_BORDER)
    tb_td = slide6.shapes.add_textbox(Inches(9.75), Inches(3.9), Inches(1.6), Inches(0.8))
    tf = tb_td.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "TEACHER DECIDES\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "Accept · modify · reject"
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = NAVY

    # Connecting horizontal line
    conn = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.4), Inches(3.0), Inches(0.6), Inches(0.02))
    conn.fill.solid()
    conn.fill.fore_color.rgb = GRAY_LINE
    conn.line.fill.background()

    conn2 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.9), Inches(3.0), Inches(0.5), Inches(0.02))
    conn2.fill.solid()
    conn2.fill.fore_color.rgb = GRAY_LINE
    conn2.line.fill.background()

    conn3 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.2), Inches(3.0), Inches(0.4), Inches(0.02))
    conn3.fill.solid()
    conn3.fill.fore_color.rgb = GRAY_LINE
    conn3.line.fill.background()

    # Bottom 4 Ablation Cards
    tb = slide6.shapes.add_textbox(Inches(0.6), Inches(5.1), Inches(8), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "— ABLATIONS — RUN ON BOTH PLAN A AND PLAN B"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = GRAY_TEXT

    ablations = [
        ("v1", "BASELINE", "discourse_text only", "Pure text baseline"),
        ("v2", "+ TYPE", "+ discourse_type", "Does type info help?"),
        ("v3", "+ LENGTH", "+ length features", "Complexity as signal?"),
        ("v4", "+ PROMPT", "+ prompt_name", "Check for leakage"),
    ]
    aw = 2.85
    for i, (v, tag, title, sub) in enumerate(ablations):
        ax = 0.6 + i * (aw + 0.22)
        add_card(slide6, ax, 5.4, aw, 1.25, CARD_BG, CARD_BORDER)
        tb_a = slide6.shapes.add_textbox(Inches(ax + 0.15), Inches(5.5), Inches(aw - 0.3), Inches(1.05))
        tf = tb_a.text_frame
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = f"{v}           {tag}\n"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = BLUE
        r2 = p.add_run()
        r2.text = title + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(13)
        r2.font.bold = True
        r2.font.color.rgb = NAVY
        r3 = p.add_run()
        r3.text = sub
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = GRAY_TEXT

    add_footer(slide6, "Supports — Criterion 03 · LR/SVM search: C in {0.01, 0.1, 1, 10}", "Plan C — Optional Extension")
    add_notes(slide6, "Feature engineering combines three streams: discourse text TF-IDF, discourse type one-hot encoding, and text length statistics. We systematically ablate each stream to isolate its contribution.")

    # =========================================================================
    # SLIDE 7: Evaluation & Risks
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_top_bar(slide7, "06 / EVALUATION & RISKS", "07")
    add_title(slide7, [
        ("Measure what matters, ", NAVY, True, 28),
        ("name what could go wrong.", ORANGE, True, 28)
    ], top=0.7)

    # Top 4 Metric Cards
    metrics = [
        ("METRIC 01", "PRIMARY", "Macro-F1", "Penalizes ignoring minority classes.", NAVY_CARD, None, WHITE, BLUE_MUTED),
        ("METRIC 02", "CRITICAL", "Recall\n(Ineffective)", "The class teachers need most — must not miss.", LIGHT_RED_BG, RED, RED, RED),
        ("METRIC 03", None, "QWK", "Ordinal agreement — penalizes ends-vs-middles.", CARD_BG, CARD_BORDER, NAVY, GRAY_TEXT),
        ("METRIC 04", None, "Confusion\nmatrix", "Diagnostic — where do we confuse?", CARD_BG, CARD_BORDER, NAVY, GRAY_TEXT)
    ]
    mw = 2.85
    for i, (m_tag, badge, m_title, m_desc, bg_m, brd_m, val_clr, tag_clr) in enumerate(metrics):
        mx = 0.6 + i * (mw + 0.22)
        add_card(slide7, mx, 1.85, mw, 1.5, bg_m, brd_m, border_width=1.5 if badge == "CRITICAL" else 1)
        tb_m = slide7.shapes.add_textbox(Inches(mx + 0.15), Inches(1.95), Inches(mw - 0.3), Inches(1.3))
        tf = tb_m.text_frame
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = m_tag
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = tag_clr
        if badge:
            r2 = p.add_run()
            r2.text = f"            [{badge}]"
            r2.font.size = Pt(7)
            r2.font.bold = True
            r2.font.color.rgb = tag_clr
        p.add_run().text = "\n"

        p2 = tf.add_paragraph()
        r3 = p2.add_run()
        r3.text = m_title
        r3.font.name = FONT_HEADING
        r3.font.size = Pt(17)
        r3.font.bold = True
        r3.font.color.rgb = val_clr
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        r4 = p3.add_run()
        r4.text = m_desc
        r4.font.size = Pt(8)
        r4.font.color.rgb = GRAY_MUTED if bg_m == NAVY_CARD else (RED if badge == "CRITICAL" else GRAY_TEXT)

    # Middle Left: Baselines We Must Beat
    tb = slide7.shapes.add_textbox(Inches(0.6), Inches(3.6), Inches(5.8), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "— BASELINES WE MUST BEAT"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT

    table_shape = slide7.shapes.add_table(3, 4, Inches(0.6), Inches(3.9), Inches(5.8), Inches(1.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.2)
    table.columns[3].width = Inches(1.2)

    headers = ["BASELINE", "ACCURACY", "MACRO-F1", "RECALL (INEFF)"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.runs[0].font.size = Pt(7)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = GRAY_TEXT

    b_rows = [
        ("Majority class", "~79.3%", "~0.29", "0%"),
        ("Random stratified", "~66%", "~0.33", "~4.5%")
    ]
    for r_idx, row in enumerate(b_rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE
            p = cell.text_frame.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            p.runs[0].font.color.rgb = NAVY if c_idx != 3 else RED
            if c_idx == 3: p.runs[0].font.bold = True

    tb_note = slide7.shapes.add_textbox(Inches(0.6), Inches(5.2), Inches(5.8), Inches(0.4))
    p = tb_note.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "Predicting 'Adequate' always → 79.3% accuracy but 0% Recall on Ineffective. "
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.color.rgb = GRAY_TEXT
    r2 = p.add_run()
    r2.text = "Accuracy alone is meaningless here."
    r2.font.size = Pt(7.5)
    r2.font.bold = True
    r2.font.color.rgb = RED

    # Middle Right: 4 Risks (2x2)
    tb = slide7.shapes.add_textbox(Inches(6.8), Inches(3.6), Inches(5.9), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "— FOUR RISKS AND HOW WE ADDRESS EACH"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT

    risks = [
        ("RISK · 01", "Miss Ineffective → no feedback", "Class weights, threshold tuning, low-confidence warnings.", ORANGE),
        ("RISK · 02", "Anchoring bias", "Suggestion, not verdict — teacher actively accepts or rejects.", ORANGE),
        ("RISK · 03", "Demographic bias", "Per-subgroup metrics. Never use demographics as inputs.", BLUE),
        ("RISK · 04", "Prompt overfit", "Leave-one-prompt-out evaluation for generalization.", GREEN),
    ]
    rw = 2.85
    rh = 0.95
    coords = [(6.8, 3.9), (9.85, 3.9), (6.8, 4.95), (9.85, 4.95)]
    for (rx, ry), (rtag, rname, rmit, rclr) in zip(coords, risks):
        add_card(slide7, rx, ry, rw, rh, CARD_BG, CARD_BORDER)
        # Left line
        ll = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(rx), Inches(ry), Inches(0.04), Inches(rh))
        ll.fill.solid()
        ll.fill.fore_color.rgb = rclr
        ll.line.fill.background()

        tb_r = slide7.shapes.add_textbox(Inches(rx + 0.12), Inches(ry + 0.08), Inches(rw - 0.2), Inches(rh - 0.15))
        tf = tb_r.text_frame
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = rtag + "\n"
        r.font.size = Pt(7)
        r.font.bold = True
        r.font.color.rgb = rclr
        r2 = p.add_run()
        r2.text = rname + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = NAVY
        r3 = p.add_run()
        r3.text = rmit
        r3.font.size = Pt(7.5)
        r3.font.color.rgb = GRAY_TEXT

    # Bottom Core Principle Box (Dark Navy)
    add_card(slide7, 0.6, 6.0, 12.1, 0.85, NAVY_CARD, None)
    tb_cp = slide7.shapes.add_textbox(Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.75))
    tf = tb_cp.text_frame
    p = tf.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "[i]  CORE PRINCIPLE\n"
    p.runs[0].font.size = Pt(7.5)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE_MUTED
    r2 = p.add_run()
    r2.text = "A screening support tool — not an automatic grader. "
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    r3 = p.add_run()
    r3.text = "Teacher always has the final say."
    r3.font.name = FONT_HEADING
    r3.font.size = Pt(13)
    r3.font.bold = True
    r3.font.color.rgb = BLUE_MUTED

    add_footer(slide7, "Criteria — 04 Evaluation (15 marks) + 05 Risks (10 marks) · Stratified GroupKFold", "")
    add_notes(slide7, "Evaluation focuses on Macro-F1 and Recall on Ineffective. Accuracy is meaningless on 79.3% majority class. We proactively address anchoring bias, demographic fairness, and prompt leakage.")

    # =========================================================================
    # SLIDE 8: Summary & References
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_top_bar(slide8, "07 / SUMMARY & REFERENCES", "08")
    add_title(slide8, [
        ("What we built, in one frame — and\n", NAVY, True, 26),
        ("where to read more.", BLUE, True, 26)
    ], top=0.7)

    # Left Summary Table
    table_shape = slide8.shapes.add_table(12, 2, Inches(0.6), Inches(1.8), Inches(7.5), Inches(4.9))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(5.7)

    table.cell(0, 0).text = "ASPECT"
    table.cell(0, 1).text = "DECISION"
    for c in [0, 1]:
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_CARD
        p = cell.text_frame.paragraphs[0]
        p.runs[0].font.size = Pt(8)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = WHITE

    summary_rows = [
        ("Problem", "Help teachers evaluate argument component quality", NAVY),
        ("User", "English writing teacher, grades 6–12", NAVY),
        ("Dataset", "PERSUADE 2.0 · 25,994 essays · 285,383 elements · CC BY 4.0", NAVY),
        ("Data split", "Train 15,593 essays · Test 10,402 essays · both in hand", NAVY),
        ("ML task", "Multi-class: Ineffective · Adequate · Effective (3 ordinal classes)", NAVY),
        ("Plan A", "TF-IDF + Logistic Regression — interpretable baseline", NAVY),
        ("Plan B", "TF-IDF + Linear SVM — stronger classical alternative", NAVY),
        ("Extension", "BERT/DeBERTa fine-tuning (if A + B complete)", GREEN),
        ("Metrics", "Macro-F1 primary · Recall (Ineffective) critical · QWK", NAVY),
        ("Baseline", "Majority class → Macro-F1 ~0.26 · Recall (Ineff) = 0%", NAVY),
        ("AI role", "Suggestion — teacher always decides", ORANGE),
    ]
    for r_idx, (asp, dec, clr) in enumerate(summary_rows):
        row = r_idx + 1
        table.cell(row, 0).text = asp
        table.cell(row, 1).text = dec
        bg_col = CARD_BG if row % 2 == 1 else RGBColor(248, 250, 252)
        for c in [0, 1]:
            cell = table.cell(row, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            p.runs[0].font.bold = (c == 0 or clr != NAVY)
            p.runs[0].font.color.rgb = clr if c == 1 else (clr if clr != NAVY else NAVY)

    # Right 4 Reference Cards
    tb = slide8.shapes.add_textbox(Inches(8.4), Inches(1.5), Inches(4.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "— KEY REFERENCES"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT

    references = [
        ("[1]", "Baffour, Saxberg & Crossley (2023)",
         "Analyzing bias in LLM-assisted writing feedback · BEA 2023",
         "DOI 10.18653/v1/2023.bea-1.21"),
        ("[2]", "Crossley et al. (2024)",
         "A large-scale corpus: PERSUADE 2.0 · Assessing Writing 61",
         "github.com / scrosseye / persuade_corpus_2.0"),
        ("[3]", "Ding, Bexte & Horbach (2023)",
         "Score it all together · Findings of ACL",
         "DOI 10.18653/v1/2023.findings-acl.825"),
        ("[4]", "Favero et al. (2026)",
         "Leveraging small LLMs for argument mining · CEUR-WS 4166",
         "ceur-ws.org / Vol-4166"),
    ]
    ref_y = 1.8
    for num, auth, pub, link in references:
        add_card(slide8, 8.4, ref_y, 4.3, 1.1, CARD_BG, CARD_BORDER)
        tb_ref = slide8.shapes.add_textbox(Inches(8.55), Inches(ref_y + 0.1), Inches(4.0), Inches(0.95))
        tf = tb_ref.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = f"{num}  "
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = BLUE
        r2 = p.add_run()
        r2.text = auth + "\n"
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = NAVY
        r3 = p.add_run()
        r3.text = pub + "\n"
        r3.font.size = Pt(8)
        r3.font.italic = True
        r3.font.color.rgb = GRAY_TEXT
        r4 = p.add_run()
        r4.text = link
        r4.font.size = Pt(7.5)
        r4.font.color.rgb = BLUE
        ref_y += 1.25

    add_footer(slide8, "APA 7 references · URLs shown as plain text — see GitHub repository", "")
    add_notes(slide8, "In summary: a grounded problem, rich dataset, classical baseline and alternative with solid theory, rigorous metrics, and awareness of ethical risks.")

    # =========================================================================
    # SLIDE 9: Closing — Q&A
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)

    # Right concentric target circles with Question mark
    for r, (fill, border) in zip(radii, colors):
        c = slide9.shapes.add_shape(MSO_SHAPE.OVAL, 
                                    Inches(circle_center_x - r), 
                                    Inches(circle_center_y - r), 
                                    Inches(r * 2), Inches(r * 2))
        if fill:
            c.fill.solid()
            c.fill.fore_color.rgb = fill
        else:
            c.fill.background()
        if border:
            c.line.color.rgb = border
            c.line.width = Pt(1.5)
        else:
            c.line.fill.background()

    # Big question mark
    tb_q = slide9.shapes.add_textbox(Inches(circle_center_x - 1.0), Inches(circle_center_y - 1.2), Inches(2.0), Inches(2.4))
    p = tb_q.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "?"
    r.font.name = FONT_HEADING
    r.font.size = Pt(90)
    r.font.bold = True
    r.font.color.rgb = WHITE

    add_top_bar(slide9, "CLOSING — Q&A", "09")

    # Big Thank you Title
    tb_title = slide9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.5), Inches(2.4))
    tf = tb_title.text_frame
    p1 = tf.paragraphs[0]
    p1.margin_left = 0
    r1 = p1.add_run()
    r1.text = "Thank\n"
    r1.font.name = FONT_HEADING
    r1.font.size = Pt(72)
    r1.font.bold = True
    r1.font.color.rgb = NAVY

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "you."
    r2.font.name = FONT_HEADING
    r2.font.size = Pt(72)
    r2.font.bold = True
    r2.font.color.rgb = BLUE

    # Subtitle
    tb_sub = slide9.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(7.5), Inches(0.9))
    tf = tb_sub.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.margin_left = 0
    r = p.add_run()
    r.text = "Questions, push-back, things we missed — they are why this deck exists."
    r.font.name = FONT_BODY
    r.font.size = Pt(16)
    r.font.color.rgb = NAVY

    # Bottom 3 Questions Cards
    tb_p = slide9.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(6.0), Inches(0.3))
    p = tb_p.text_frame.paragraphs[0]
    p.margin_left = 0
    p.add_run().text = "— PREPARED FOR LIKELY QUESTIONS"
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = GRAY_TEXT

    q_cards = [
        ("Q · 01", "Is BERT definitely better than LR?"),
        ("Q · 02", "Why LR + SVM, not Random Forest?"),
        ("Q · 03", "What if Recall is too low to ship?")
    ]
    qw = 2.4
    for i, (qnum, qtxt) in enumerate(q_cards):
        qx = 0.8 + i * (qw + 0.25)
        # Line top
        top_line = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(qx), Inches(5.8), Inches(qw), Inches(0.02))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = GRAY_LINE
        top_line.line.fill.background()

        tb_qc = slide9.shapes.add_textbox(Inches(qx), Inches(5.9), Inches(qw), Inches(0.8))
        tf = tb_qc.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.margin_left = 0
        r = p.add_run()
        r.text = qnum + "\n"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = GRAY_TEXT
        r2 = p.add_run()
        r2.text = qtxt
        r2.font.name = FONT_HEADING
        r2.font.size = Pt(10.5)
        r2.font.bold = True
        r2.font.color.rgb = NAVY

    add_footer(slide9, "61FIT4MLA · Midterm · Fall 2026", "Criterion — 06 Communication (10 marks)")
    add_notes(slide9, "Thank you for listening. We welcome any questions and feedback on our problem formulation, data strategies, and evaluation plan.")

    output_path = "presentation_editable.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_presentation()
