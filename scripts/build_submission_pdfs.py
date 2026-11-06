"""
AegisEdge Master Submission PDF Builder
Compiles both official Stage 1 submission PDF documents:
1. outputs/AegisEdge_Project_Proposal_PS2.pdf (Full Academic Proposal Document)
2. outputs/AegisEdge_Executive_Deck_and_Benchmarks.pdf (Executive Deck & Benchmark Evidence)

Strictly adhering to academic submission requirements:
- Times New Roman typography (Times-Roman body, Times-Bold headings only)
- Fully justified text alignment
- Pure black-and-white table styling (no black header fills)
- Publication-grade STIX mathematical equations (right-tagged)
- User-uploaded architecture infographic embedded
- High-resolution visual demonstration figures
- No running headers or footers
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

from generate_perfect_proposal_pdf import build_perfect_proposal
from generate_perfect_deck_pdf import build_executive_deck_pdf


def main():
    print("=" * 80)
    print("AegisEdge: Compiling Both Submission PDF Documents")
    print("Namma AI Hackathon 2026 — Problem Statement 2 (Safer Communities)")
    print("=" * 80)

    # 1. Proposal Document
    build_perfect_proposal()

    # 2. Executive Deck & Benchmarks Document
    build_executive_deck_pdf()

    print("\n" + "=" * 80)
    print("[+] ALL SUBMISSION ASSETS SUCCESSFULLY GENERATED & VERIFIED!")
    print("    1. Technical Proposal PDF : outputs/AegisEdge_Project_Proposal_PS2.pdf")
    print("    2. Executive Deck PDF     : outputs/AegisEdge_Executive_Deck_and_Benchmarks.pdf")
    print("=" * 80)


if __name__ == "__main__":
    main()
