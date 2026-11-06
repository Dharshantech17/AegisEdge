"""
AegisEdge System Architecture Diagram Generator
Generates a high-resolution, publication-grade system architecture diagram (PNG).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DIAGRAM_PATH = os.path.join(OUTPUT_DIR, "overall_architecture_diagram.png")


def create_diagram():
    print(f"[*] Rendering Overall Architecture Diagram to: {DIAGRAM_PATH}...")
    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Color definitions
    C_BLUE = '#0284C7'       # Sky Blue
    C_BLUE_BG = '#F0F9FF'
    C_GREEN = '#16A34A'      # Emerald Green
    C_GREEN_BG = '#F0FDF4'
    C_PURPLE = '#7C3AED'     # Purple
    C_PURPLE_BG = '#FAF5FF'
    C_AMBER = '#D97706'      # Amber
    C_AMBER_BG = '#FFFBEB'
    C_DARK = '#1E293B'
    C_GRAY = '#64748B'

    def draw_box(x, y, w, h, title, subtitle="", border_color=C_BLUE, bg_color=C_BLUE_BG, lw=1.5, radius=0.15):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=patches.BoxStyle("Round", pad=0.08, rounding_size=radius),
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=lw,
            zorder=3
        )
        ax.add_patch(box)
        if title:
            y_title = y + h * 0.58 if subtitle else y + h * 0.5
            ax.text(x + w / 2, y_title, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold', color=C_DARK, zorder=4)
        if subtitle:
            ax.text(x + w / 2, y + h * 0.28, subtitle, ha='center', va='center',
                    fontsize=8.0, color=C_GRAY, zorder=4)

    def draw_arrow(x1, y1, x2, y2, color=C_DARK, style='->', lw=1.5):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0),
            zorder=2
        )

    # 1. Input Node
    draw_box(0.5, 4.8, 2.2, 1.2, "Supplied Traffic Media", "10-20s Clip / Images\n(320x320 RGB)", border_color=C_BLUE, bg_color=C_BLUE_BG)

    # Arrow to Preprocessing
    draw_arrow(2.7, 5.4, 3.2, 5.4)

    # 2. Preprocessing
    draw_box(3.2, 4.8, 2.2, 1.2, "Preprocessing Engine", "Resize & Normalization\nVolatile RAM Tensor", border_color=C_BLUE, bg_color=C_BLUE_BG)

    # Arrow to Runtime
    draw_arrow(5.4, 5.4, 5.9, 5.4)

    # 3. ExecuTorch Runtime
    draw_box(5.9, 4.8, 2.5, 1.2, "Meta ExecuTorch 0.4+", "Arm XNNPACK Backend\nTarget: Cortex-A76 (Pi 5)", border_color=C_PURPLE, bg_color=C_PURPLE_BG, lw=2.0)

    # Arrow down into Complete Neural Network
    draw_arrow(7.15, 4.8, 7.15, 4.1)

    # 4. Complete Neural Network Group (Container)
    net_bg = patches.FancyBboxPatch(
        (0.5, 2.4), 11.0, 1.7,
        boxstyle=patches.BoxStyle("Round", pad=0.1, rounding_size=0.2),
        facecolor='#F8FAFC',
        edgecolor='#94A3B8',
        linewidth=1.2,
        linestyle='--',
        zorder=1
    )
    ax.add_patch(net_bg)
    ax.text(0.7, 3.85, "COMPLETE SSDLITE320-MOBILENETV3 NEURAL COMPUTATION GRAPH (EXPORTED: models/complete_detector_net.pt, 14.76 MB)",
            fontsize=8.5, fontweight='bold', color='#475569', zorder=2)

    # Backbone inside
    draw_box(1.0, 2.65, 3.0, 1.0, "MobileNetV3 Backbone", "Feature Pyramid Network (FPN)", border_color=C_PURPLE, bg_color=C_PURPLE_BG)

    # Arrows to Heads
    draw_arrow(4.0, 3.3, 4.6, 3.45)
    draw_arrow(4.0, 3.0, 4.6, 2.85)

    # Multi-Scale Heads
    draw_box(4.6, 3.2, 3.3, 0.65, "Multi-Scale Box Heads", "Output: [1, 3234, 4] Tensor", border_color=C_PURPLE, bg_color=C_PURPLE_BG)
    draw_box(4.6, 2.45, 3.3, 0.65, "Multi-Scale Class Heads", "Output: [1, 3234, 91] Tensor", border_color=C_PURPLE, bg_color=C_PURPLE_BG)

    # Arrows to Post-Processing
    draw_arrow(7.9, 3.52, 8.4, 3.2)
    draw_arrow(7.9, 2.78, 8.4, 3.1)

    # Anchor Decoding & NMS
    draw_box(8.4, 2.65, 2.8, 1.0, "Anchor Decoding & NMS", "Vector Box Regression\nThreshold: IoU 0.45", border_color=C_PURPLE, bg_color=C_PURPLE_BG)

    # Arrow down to Deliverables split
    draw_arrow(9.8, 2.4, 9.8, 2.0)
    draw_arrow(9.8, 2.0, 3.6, 2.0)
    draw_arrow(3.6, 2.0, 3.6, 1.6)
    draw_arrow(9.8, 2.0, 9.2, 1.6)

    # 5. Core Mandatory Deliverables (Green Box)
    core_bg = patches.FancyBboxPatch(
        (0.5, 0.3), 6.2, 1.3,
        boxstyle=patches.BoxStyle("Round", pad=0.08, rounding_size=0.15),
        facecolor=C_GREEN_BG,
        edgecolor=C_GREEN,
        linewidth=1.8,
        zorder=3
    )
    ax.add_patch(core_bg)
    ax.text(3.6, 1.35, "PRIMARY MANDATORY DELIVERABLES (CORE GUARANTEED)", ha='center', fontsize=9.0, fontweight='bold', color=C_GREEN, zorder=4)
    ax.text(3.6, 1.05, "• Category-Wise Counter: Per-frame & cumulative counts (Person vs Vehicles)", ha='center', fontsize=7.8, color=C_DARK, zorder=4)
    ax.text(3.6, 0.78, "• Annotated Outputs: Visual bounding boxes, labels, and ground-contact dots", ha='center', fontsize=7.8, color=C_DARK, zorder=4)
    ax.text(3.6, 0.50, "• Performance Benchmarking: Mean/p95 latency (ms) & system throughput (FPS)", ha='center', fontsize=7.8, color=C_DARK, zorder=4)

    # 6. Secondary Differentiator (Amber Box)
    diff_bg = patches.FancyBboxPatch(
        (7.0, 0.3), 4.5, 1.3,
        boxstyle=patches.BoxStyle("Round", pad=0.08, rounding_size=0.15),
        facecolor=C_AMBER_BG,
        edgecolor=C_AMBER,
        linewidth=1.8,
        zorder=3
    )
    ax.add_patch(diff_bg)
    ax.text(9.25, 1.35, "SECONDARY HEURISTIC DIFFERENTIATOR", ha='center', fontsize=9.0, fontweight='bold', color=C_AMBER, zorder=4)
    ax.text(9.25, 1.05, "• Heuristic Conflict Exposure Duration: CED = sum[ I(t) * delta_t ]", ha='center', fontsize=7.8, color=C_DARK, zorder=4)
    ax.text(9.25, 0.78, "• Ground-Contact Calibration: Bottom-center ((x1+x2)/2, y2)", ha='center', fontsize=7.8, color=C_DARK, zorder=4)
    ax.text(9.25, 0.50, "• Lateral Corridor Proximity (|xp - xv| / W <= 0.35) & 6-Frame Debounce", ha='center', fontsize=7.8, color=C_DARK, zorder=4)

    plt.tight_layout()
    plt.savefig(DIAGRAM_PATH, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully rendered Architecture Diagram: {DIAGRAM_PATH}")


if __name__ == "__main__":
    create_diagram()

