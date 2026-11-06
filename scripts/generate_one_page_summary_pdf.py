#!/usr/bin/env python3
"""
AegisEdge: Minimalist One-Page Executive Submission Document
Problem Statement 2: AI for Safer Communities (Namma AI Hackathon 2026)
Generates: outputs/AegisEdge_OnePage_Executive_Summary_PS2.pdf

STRICTLY 1 PAGE. Clean, spacious, and de-congested.
Uses: outputs/AegisEdge AI Architecture Infographic.png
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
PDF_PATH = os.path.join(OUTPUT_DIR, "AegisEdge_OnePage_Executive_Summary_PS2.pdf")

DRIVE_LINK = "https://drive.google.com/drive/folders/1TI-24bI7EP6mereBzB6yHRrzYKseYXGi?usp=sharing"
GITHUB_LINK = "https://github.com/Dharshantech17/AegisEdge"
INFOGRAPHIC_PATH = os.path.join(OUTPUT_DIR, "AegisEdge AI Architecture Infographic.png")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 30, 612 - 40, 30)
        
        self.drawString(40, 18, "Namma AI Hackathon 2026 — Problem Statement 2 (AI for Safer Communities)")
        self.drawRightString(612 - 40, 18, "AegisEdge Master Submission Document")
        self.restoreState()

def build_pdf():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        alignment=0
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#475569'),
        alignment=0
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.0,
        leading=13.0,
        textColor=colors.HexColor('#1E293B'),
        alignment=0
    )
    caption_style = ParagraphStyle(
        'Caption',
        fontName='Helvetica-Oblique',
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor('#64748B'),
        alignment=1 # Centered
    )

    story = []

    # 1. Header Block (Using exact requested wording)
    story.append(Paragraph("AegisEdge: Privacy-Preserving Edge AI Architecture", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Problem Statement 2: AI for Safer Communities — Edge-Based Object Detection and Counting", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Organizers:</b> Nasscom CoE – IoT & AI | Arm | IIIT Bangalore | Supported by UK-India TSI<br/>"
        "<b>Target Platform:</b> Raspberry Pi 5 (Quad-Core Arm Cortex-A76 @ 2.4 GHz) | <b>Runtime:</b> Meta ExecuTorch 0.4+ (Arm XNNPACK)<br/>"
        "<b>System Architect & Contributor:</b> Dharshan S (Dharshantech17 | dharshanselva2006@gmail.com)",
        meta_style
    ))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#0284C7"), spaceAfter=10, spaceBefore=2))

    # 2. Prominent Architecture Infographic
    story.append(Paragraph("AegisEdge AI Architecture Infographic", h1_style))
    story.append(Spacer(1, 4))

    target_w = 520
    with PILImage.open(INFOGRAPHIC_PATH) as im:
        orig_w, orig_h = im.size
        aspect = orig_w / float(orig_h)
        target_h = target_w / aspect

    if target_h > 280:
        target_h = 280
        target_w = target_h * aspect

    img_table = Table([[Image(INFOGRAPHIC_PATH, width=target_w, height=target_h)]], colWidths=[532])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(img_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Figure 1: AegisEdge AI Architecture Infographic — End-to-End Pipeline on Arm Cortex-A76 with Heuristic CED & Volatile DDR Privacy.", caption_style))
    
    story.append(Spacer(1, 14))

    # 3. Master Google Drive Submission Box (With "Demo Video")
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
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_drive)

    story.append(Spacer(1, 10))

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
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_git)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] SUCCESS! Clean One-Page Summary PDF compiled at:")
    print(f"    --> {PDF_PATH}")
    print(f"    File Size: {os.path.getsize(PDF_PATH) / 1024:.1f} KB")

if __name__ == "__main__":
    build_pdf()
