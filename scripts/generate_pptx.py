"""
AegisEdge Professional PowerPoint Deck Generator (16:9 Widescreen PPTX)
Creates an 8-slide executive pitch presentation for Namma AI Hackathon 2026 PS2.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
PPTX_PATH = os.path.join(OUTPUT_DIR, "AegisEdge_Presentation_Deck.pptx")
QC_DIR = os.path.join(OUTPUT_DIR, "qc_frames")

# Color Palette (Dark Theme / Professional Executive)
BG_DARK = RGBColor(15, 23, 42)        # Slate 900
CARD_BG = RGBColor(30, 41, 59)        # Slate 800
ACCENT_BLUE = RGBColor(14, 165, 233)   # Sky Blue
ACCENT_GOLD = RGBColor(245, 158, 11)   # Amber Gold
ACCENT_GREEN = RGBColor(34, 197, 94)   # Emerald Green
TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_MUTED = RGBColor(148, 163, 184)   # Slate 400
TEXT_LIGHT = RGBColor(226, 232, 240)   # Slate 200
BORDER_COLOR = RGBColor(51, 65, 85)    # Slate 700


def create_base_slide(prs, title_text, category_tag="NAMMA AI HACKATHON 2026 | PROBLEM STATEMENT 2"):
    """Creates a blank slide with dark background, header banner, and footer."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Background rectangle
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()

    # Top accent line
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ACCENT_BLUE
    top_bar.line.fill.background()

    if title_text:
        # Category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_GOLD

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "AegisEdge | Arm Cortex-A76 (Raspberry Pi 5) | Meta ExecuTorch (XNNPACK) | Nasscom CoE - IoT & AI | UK-India TSI"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = TEXT_MUTED

    return slide


def add_card(slide, left, top, width, height, title, bg_color=CARD_BG, border_color=BORDER_COLOR):
    """Adds a rounded rectangle card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = title.upper()
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

    return card


def build_deck():
    print(f"[*] Initializing Presentation Deck (16:9 Widescreen)...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    slide1 = create_base_slide(prs, "")
    
    # Big Title Box
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "NAMMA AI HACKATHON 2026 | PROBLEM STATEMENT 2"
    p0.font.name = "Arial"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GOLD
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "AegisEdge"
    p1.font.name = "Arial"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Privacy-Preserving Edge AI for Pedestrian and Vehicle Counting with Crosswalk Conflict-Exposure Analytics"
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_BLUE

    # 4 Key Spec Badges
    specs = [
        ("PRIMARY TARGET", "Raspberry Pi 5\n(Arm Cortex-A76)", ACCENT_GREEN),
        ("RUNTIME", "Meta ExecuTorch 0.4+\n(Arm XNNPACK Backend)", ACCENT_BLUE),
        ("CORE DELIVERABLE", "Category Counting &\nBenchmarking (Latency/FPS)", ACCENT_GOLD),
        ("DIFFERENTIATOR", "Heuristic Conflict\nExposure Duration (CED)", RGBColor(236, 72, 153))
    ]
    card_w = Inches(2.65)
    card_h = Inches(1.5)
    start_x = Inches(1.0)
    start_y = Inches(4.3)

    for i, (tag, val, col) in enumerate(specs):
        bx = start_x + i * (card_w + Inches(0.24))
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, start_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = slide1.shapes.add_textbox(bx + Inches(0.15), start_y + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
        tf_b = tb.text_frame
        p_t = tf_b.paragraphs[0]
        p_t.text = tag
        p_t.font.name = "Arial"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(6)

        p_v = tf_b.add_paragraph()
        p_v.text = val
        p_v.font.name = "Arial"
        p_v.font.size = Pt(13)
        p_v.font.bold = True
        p_v.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 2: Problem Grounding (Cloud CCTV vs Edge AI)
    # -------------------------------------------------------------
    slide2 = create_base_slide(prs, "Problem Context: Conventional Cloud Surveillance Fails")
    
    # Left Card: Cloud CCTV
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0), "Conventional Cloud Surveillance Flaws", border_color=RGBColor(239, 68, 68))
    tb_l = slide2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.1))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    cloud_points = [
        ("High Cellular Bandwidth Cost:", "Streaming 24/7 high-definition video over cellular modems incurs severe, recurring monthly data expenses for municipal bodies."),
        ("High Round-Trip Latency:", "Cloud inference loops introduce 1-3 second round-trip delays, preventing responsive telemetry."),
        ("Citizen Privacy & DPDP Compliance:", "Streaming identifiable citizen footage to remote servers introduces grave surveillance risks and legal liabilities."),
        ("Passive Counting Only:", "Simple raw counts do not reveal vulnerable road user (VRU) conflict exposure or unsafe crossing conditions.")
    ]
    for i, (title, desc) in enumerate(cloud_points):
        p_h = tf_l.paragraphs[0] if i == 0 else tf_l.add_paragraph()
        p_h.text = f"• {title} "
        p_h.font.bold = True
        p_h.font.size = Pt(11.5)
        p_h.font.color.rgb = RGBColor(248, 113, 113)
        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(10)

    # Right Card: AegisEdge Focused Edge Solution
    add_card(slide2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.0), "AegisEdge: Focused On-Device Architecture", border_color=ACCENT_GREEN)
    tb_r = slide2.shapes.add_textbox(Inches(7.1), Inches(2.3), Inches(5.2), Inches(4.1))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    edge_points = [
        ("100% On-Chip Ingestion & Processing:", "All frame decoding and neural tensor operations run locally in volatile RAM on the Arm Cortex-A76 processor."),
        ("Mandatory Deliverables Priority:", "Guaranteed per-frame and cumulative category counting for pedestrians and vehicles, plus empirical latency/FPS benchmarking."),
        ("Heuristic Conflict Exposure Duration (CED):", "Empirically calculates cumulative shared-zone co-occupancy duration (seconds) without expensive tracking."),
        ("Privacy-by-Design:", "Zero raw video exfiltration. Zero facial recognition or vehicle license plate reading (ANPR).")
    ]
    for i, (title, desc) in enumerate(edge_points):
        p_h = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p_h.text = f"• {title} "
        p_h.font.bold = True
        p_h.font.size = Pt(11.5)
        p_h.font.color.rgb = ACCENT_GREEN
        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: Technical Architecture & Complete Model Export
    # -------------------------------------------------------------
    slide3 = create_base_slide(prs, "Technical Architecture: Complete SSDLite Neural Export")

    # Overview box
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.1), "Core Engineering Philosophy: Complete Graph Lowering")
    tb_arch = slide3.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.3), Inches(0.5))
    tf_arch = tb_arch.text_frame
    p_arch = tf_arch.paragraphs[0]
    p_arch.text = "Unlike naive submissions that only export the feature backbone, AegisEdge captures the complete SSDLite320-MobileNetV3 computation graph—including the MobileNetV3 feature pyramid, multiscale box regression heads [1, 3234, 4], and classification heads [1, 3234, 91] (14.76 MB .pt artifact verified)."
    p_arch.font.size = Pt(11)
    p_arch.font.color.rgb = TEXT_LIGHT

    # 3 Architecture Steps
    steps = [
        ("1. Input & Lowering", [
            "Ingests 10-20s video clips (MP4/AVI) or image sequences (320x320 RGB).",
            "Lowered via Meta ExecuTorch 0.4+ using the Arm XNNPACK partitioner.",
            "Targeting INT8 quantized .pte binary for Cortex-A76."
        ], ACCENT_BLUE),
        ("2. Detection & Post-Processing", [
            "Simultaneous multiscale anchor box regression across 6 feature scales.",
            "Vectorized anchor box decoding & lightweight Non-Maximum Suppression (NMS).",
            "Extracts person, car, bus, truck, and motorcycle detections."
        ], ACCENT_GOLD),
        ("3. Mandatory & Value-Add Output", [
            "Category-wise per-frame and cumulative object counting engine.",
            "Optional temporal tracking (short-duration 15-frame retention window).",
            "Heuristic CED accumulator & automated JSON benchmark reporting."
        ], ACCENT_GREEN)
    ]
    sw = Inches(3.7)
    sh = Inches(3.7)
    for i, (stitle, sbullets, scol) in enumerate(steps):
        sx = Inches(0.8) + i * (sw + Inches(0.3))
        add_card(slide3, sx, Inches(2.9), sw, sh, stitle, border_color=scol)
        tb_s = slide3.shapes.add_textbox(sx + Inches(0.2), Inches(3.5), sw - Inches(0.4), sh - Inches(0.8))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        for j, btext in enumerate(sbullets):
            p_b = tf_s.paragraphs[0] if j == 0 else tf_s.add_paragraph()
            p_b.text = f"• {btext}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = TEXT_LIGHT
            p_b.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 4: Main Differentiator: Heuristic Conflict Exposure
    # -------------------------------------------------------------
    slide4 = create_base_slide(prs, "Main Differentiator: Heuristic Conflict Exposure Duration (CED)")

    # Left card: The Mathematical Formulation
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0), "Heuristic Formulation & Debounce Logic")
    tb_m = slide4.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.2))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    m_points = [
        ("Transparent Heuristic Metric:", "AegisEdge does not claim to predict accidents or near-misses. It provides an objective, transparent heuristic indicator of concurrent crosswalk co-occupancy."),
        ("Ground-Contact Calibration:", "Evaluates zone occupancy at the bottom-center coordinate ((x1+x2)/2, y2), representing true physical road surface contact (feet for pedestrians, tires for vehicles)."),
        ("Source-Video Timestamp Delta:", "CED = sum[ I(t) * (t_{t+1} - t_t) ] where delta_t = 1 / FPS_video. Exposure time is physically accurate to the source clip, not skewed by edge inference speed."),
        ("Lateral Corridor Constraint:", "Co-occupancy is restricted to |xp - xv| / W_frame <= 0.35, eliminating false alarms between opposite sidewalks."),
        ("Debounce Filter:", "Groups continuous overlap frames into single episodes using a 6-frame debounce buffer.")
    ]
    for i, (title, desc) in enumerate(m_points):
        p_h = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p_h.text = f"• {title} "
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = ACCENT_GOLD
        p_d = tf_m.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(6)

    # Right Card: Deliverables Scope Boundaries
    add_card(slide4, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.0), "Deliverables Scope & Integrity Boundaries")
    tb_d = slide4.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.2), Inches(4.2))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    scope_points = [
        ("Mandatory Core Deliverables (Guaranteed):", "1. On-device object detection for pedestrians and vehicles.\n2. Frame-level and cumulative category counting.\n3. Annotated visual debug output.\n4. Empirical latency and FPS throughput reporting."),
        ("Clarification on Temporal Tracking:", "Multi-frame tracking is an optional secondary enhancement that will be incorporated during Stage 2 if implementation time permits. Per-frame detection and counting remain the core deliverable."),
        ("Explicit Exclusions (Out-of-Scope):", "• Physical traffic-light controllers and dynamic IoT actuators.\n• 24/7 continuous field surveillance.\n• Complex multi-camera sensor fusion networks.\n• Cloud-based streaming backends.")
    ]
    for i, (title, desc) in enumerate(scope_points):
        p_h = tf_d.paragraphs[0] if i == 0 else tf_d.add_paragraph()
        p_h.text = f"• {title}"
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = ACCENT_BLUE
        p_d = tf_d.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 5: Visual Demonstration & Telemetry HUD
    # -------------------------------------------------------------
    slide5 = create_base_slide(prs, "Live Demonstration: Simulated Edge Inference & HUD")

    frame_450 = os.path.join(QC_DIR, "frame_450.jpg")
    if os.path.exists(frame_450):
        slide5.shapes.add_picture(frame_450, Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.22))

    # Right Side Callout Box
    add_card(slide5, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.0), "HUD Telemetry Highlights")
    tb_hud = slide5.shapes.add_textbox(Inches(8.8), Inches(2.2), Inches(3.5), Inches(4.2))
    tf_hud = tb_hud.text_frame
    tf_hud.word_wrap = True

    hud_notes = [
        ("Multi-Class Overlays:", "Pedestrians in Green, Cars in Blue, Buses in Magenta, Motorcycles in Cyan/Yellow with individual class probabilities."),
        ("Ground Contact Dots:", "Red dots evaluated at bottom-center ((x1+x2)/2, y2) represent true road surface contact."),
        ("Dual Telemetry HUD:", "Explicitly distinguishes Host Simulation speed (~18 ms) from Stage 2 Raspberry Pi 5 Target (< 100 ms, >= 10 FPS)."),
        ("Actionable Status:", "Live banner flags SIMULTANEOUS CROSSWALK CO-OCCUPANCY ACTIVE when shared corridor co-occupancy occurs.")
    ]
    for i, (title, desc) in enumerate(hud_notes):
        p_h = tf_hud.paragraphs[0] if i == 0 else tf_hud.add_paragraph()
        p_h.text = f"• {title} "
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = ACCENT_GREEN
        p_d = tf_hud.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: Hardware Targets & Pre-Validation Table
    # -------------------------------------------------------------
    slide6 = create_base_slide(prs, "Hardware Feasibility & Proposed Engineering Targets")

    # Table of Targets
    t_shape = slide6.shapes.add_table(8, 3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
    table = t_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.7)

    headers = ["Metric / Parameter", "Proposed Engineering Target", "Stage 2 Evaluation Method"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(14, 165, 233)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    targets_data = [
        ("Target Architecture", "Arm Cortex-A76 @ 2.4 GHz (Raspberry Pi 5)", "Physical evaluation board for live demonstration"),
        ("Operating System", "64-bit Raspberry Pi OS (Debian 12 Bookworm)", "Standard AArch64 Linux for ExecuTorch runtime"),
        ("Model Inference Latency", "Target < 100 ms per frame", "Wall-clock time.perf_counter() on Raspberry Pi 5"),
        ("System Throughput", "Target >= 10 FPS sustained", "Average frame processing rate over 10-20s video clip"),
        ("Quantized Model Size", "Target < 20 MB (INT8 .pte binary)", "Physical file size of exported ExecuTorch program"),
        ("Peak RAM Footprint", "Target < 300 MB during active inference", "Measured via OS memory profiling (psutil / free -m)"),
        ("Counting Accuracy (MACE)", "Target <= 10% error against ground truth", "Mean Absolute Counting Error evaluated category-wise")
    ]

    for row_idx, row in enumerate(targets_data, start=1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(24, 33, 47)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_WHITE if col_idx == 0 else TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 7: Municipal Intelligence & Civic Impact
    # -------------------------------------------------------------
    slide7 = create_base_slide(prs, "Civic Actionability: Municipal Crosswalk Safety Report")

    frame_950 = os.path.join(QC_DIR, "frame_950.jpg")
    if os.path.exists(frame_950):
        slide7.shapes.add_picture(frame_950, Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.22))

    # Right Card: Civic Actionability
    add_card(slide7, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.0), "Municipal Decision-Making Impact")
    tb_imp = slide7.shapes.add_textbox(Inches(8.8), Inches(2.2), Inches(3.5), Inches(4.2))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True

    impact_notes = [
        ("Evidence-Based Infrastructure:", "Provides municipal engineers with concrete empirical metrics (CED and CER) to justify pedestrian refuge islands or traffic signals."),
        ("No Cloud Bandwidth Burden:", "Enables municipal transit agencies to monitor community crossings without recurring cellular carrier fees."),
        ("Zero Privacy Liabilities:", "Fully compliant with Indian DPDP principles: all video data remains in volatile edge memory and is immediately discarded."),
        ("Open-Source Civic Tooling:", "All code, documentation, and lowering scripts available on GitHub for community deployment.")
    ]
    for i, (title, desc) in enumerate(impact_notes):
        p_h = tf_imp.paragraphs[0] if i == 0 else tf_imp.add_paragraph()
        p_h.text = f"• {title} "
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = ACCENT_GOLD
        p_d = tf_imp.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 8: Summary & Hackathon Roadmap
    # -------------------------------------------------------------
    slide8 = create_base_slide(prs, "Stage 2 Roadmap & Deliverables Compliance")

    # 3 Summary Cards
    cards_data = [
        ("Stage 1 Pre-Validation (Done)", [
            "Complete detector neural graph captured: models/complete_detector_net.pt (14.76 MB).",
            "Inference pipeline tested on video and image sequence directories.",
            "Heuristic CED formula validated with source-video timestamps.",
            "Automated JSON benchmark reporting engine verified."
        ], ACCENT_GREEN),
        ("Pre-Hackathon Training Phase", [
            "Attendance of official Arm and IIIT-Bangalore technical enablement sessions.",
            "ExecuTorch AArch64 toolchain compilation flags fine-tuning.",
            "INT8 Post-Training Quantization (PTQ) benchmarking.",
            "Raspberry Pi 5 OS environment preparation."
        ], ACCENT_BLUE),
        ("Stage 2 Live Demonstration", [
            "Physical deployment on Raspberry Pi 5 hardware (Arm Cortex-A76).",
            "Execution against official organizer-supplied test clips/images.",
            "Ground-truth counting validation & MACE error calculation.",
            "Wall-clock latency & RAM benchmarking report delivery."
        ], ACCENT_GOLD)
    ]

    for i, (ctitle, cbullets, ccol) in enumerate(cards_data):
        cx = Inches(0.8) + i * (Inches(3.7) + Inches(0.3))
        add_card(slide8, cx, Inches(1.6), Inches(3.7), Inches(5.0), ctitle, border_color=ccol)
        tb_c = slide8.shapes.add_textbox(cx + Inches(0.2), Inches(2.2), Inches(3.3), Inches(4.2))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        for j, b in enumerate(cbullets):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = f"✔ {b}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(12)

    prs.save(PPTX_PATH)
    print(f"[+] Successfully generated 16:9 Presentation Deck: {PPTX_PATH}")
    print(f"    File Size: {os.path.getsize(PPTX_PATH) / 1024:.1f} KB")


if __name__ == "__main__":
    build_deck()

