#!/usr/bin/env python3
"""
AegisEdge: Minimalist One-Page Executive Submission Document
Generates: outputs/AegisEdge_OnePage_Executive_Summary_PS2.pdf

STRICTLY 1 PAGE.
Minimalist layout:
1. Title: AegisEdge — Privacy-Preserving Edge AI Architecture
2. Architecture Infographic: outputs/AegisEdge AI Architecture Infographic.png
3. Master Google Drive Link Box (clickable) with hosted deliverables summary
4. Public GitHub Repository Link Box
(Top metadata block and bottom footer removed as requested)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
PDF_PATH = os.path.join(OUTPUT_DIR, "AegisEdge_OnePage_Executive_Summary_PS2.pdf")

DRIVE_LINK = "https://drive.google.com/drive/folders/1TI-24bI7EP6mereBzB6yHRrzYKseYXGi?usp=sharing"
GITHUB_LINK = "https://github.com/Dharshantech17/AegisEdge"
INFOGRAPHIC_PATH = os.path.join(OUTPUT_DIR, "AegisEdge AI Architecture Infographic.png")

def build_pdf():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.0,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        alignment=0
    )
    caption_style = ParagraphStyle(
        'Caption',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748B'),
        alignment=1 # Centered
    )

    story = []

    # 1. Clean Title Block (No metadata lines)
    story.append(Paragraph("AegisEdge: Privacy-Preserving Edge AI Architecture", title_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284C7"), spaceAfter=14, spaceBefore=2))

    # 2. Prominent Architecture Infographic
    target_w = 532
    with PILImage.open(INFOGRAPHIC_PATH) as im:
        orig_w, orig_h = im.size
        aspect = orig_w / float(orig_h)
        target_h = target_w / aspect

    if target_h > 310:
        target_h = 310
        target_w = target_h * aspect

    img_table = Table([[Image(INFOGRAPHIC_PATH, width=target_w, height=target_h)]], colWidths=[532])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(img_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Figure 1: AegisEdge AI Architecture Infographic — End-to-End Pipeline on Arm Cortex-A76 with Heuristic CED & Volatile DDR Privacy.", caption_style))
    
    story.append(Spacer(1, 20))

    # 3. Master Google Drive Submission Box (Clean & Prominent)
    drive_content = (
        f"<font size=11 color='#0F172A'><b>MASTER GOOGLE DRIVE SUBMISSION FOLDER:</b></font><br/>"
        f"<font size=10 color='#0284C7'><b><u><a href='{DRIVE_LINK}'>{DRIVE_LINK}</a></u></b></font><br/><br/>"
        f"<font size=8.5 color='#334155'>"
        f"<b>Hosted Deliverables in this Drive Folder:</b><br/>"
        f"• <b>Demo Video:</b> <code>AegisEdge_HighQuality_Demo.mp4</code> (720p HD, 60.00s Operations Dashboard with HUD telemetry)<br/>"
        f"• <b>Complete Model Binary:</b> <code>complete_detector_net.pt</code> (14.76 MB PyTorch 2.x ExportedProgram for ExecuTorch)<br/>"
        f"• <b>Machine-Readable Telemetry:</b> <code>benchmark_report.json</code> (100-frame raw latency, FPS & counting error telemetry)<br/>"
        f"• <b>Academic Proposal Document:</b> <code>AegisEdge_Project_Proposal_PS2.pdf</code> (7-Page Proposal Document)<br/>"
        f"• <b>Executive Deck & Benchmarks:</b> <code>AegisEdge_Executive_Deck_and_Benchmarks.pdf</code> (5-Page Empirical Validation Dossier)<br/>"
        f"• <b>Sample Detection Outputs:</b> <code>sample_output_1_detection_hud.jpg</code> and <code>sample_output_2_municipal_report.jpg</code>"
        f"</font>"
    )
    t_drive = Table([[Paragraph(drive_content, body_style)]], colWidths=[532])
    t_drive.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1.25, colors.HexColor('#0284C7')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(t_drive)

    story.append(Spacer(1, 14))

    # 4. GitHub Code Repository Box
    git_content = (
        f"<font size=9.5 color='#0F172A'><b>PUBLIC GITHUB REPOSITORY (SOURCE CODE & SCRIPTS):</b></font><br/>"
        f"<font size=9.0 color='#0052CC'><b><u><a href='{GITHUB_LINK}'>{GITHUB_LINK}</a></u></b></font> &nbsp;|&nbsp; "
        f"<font size=8.0 color='#64748B'>Full Python/ExecuTorch export pipeline, latency benchmarks, and documentation.</font>"
    )
    t_git = Table([[Paragraph(git_content, body_style)]], colWidths=[532])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_git)

    # Build without footer (no onFirstPage / onLaterPages callback)
    doc.build(story)
    print(f"[+] SUCCESS! Clean One-Page Summary PDF compiled at:")
    print(f"    --> {PDF_PATH}")
    print(f"    File Size: {os.path.getsize(PDF_PATH) / 1024:.1f} KB")

if __name__ == "__main__":
    build_pdf()
