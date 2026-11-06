# AegisEdge — Official Stage 1 Submission Checklist & Mandatory Deliverables
**Namma AI Hackathon 2026**  
**Track:** Problem Statement 2 — AI for Safer Communities: Edge-Based Object Detection and Counting  
**Organizers:** Nasscom CoE – IoT & AI | Arm | IIIT Bangalore | Supported by UK-India Technology Security Initiative  

---

## 1. What You Need to Upload on the Hackathon Portal

The portal allows you to upload **2 files**. Here is the exact mapping:

### Slot 1: Executive Deck & Empirical Benchmark Report (File 1)
* **File to Upload:** `outputs/AegisEdge_Executive_Deck_and_Benchmarks.pdf`
* **File Size:** ~561 KB (5 Pages)
* **What it contains:**
  * Executive Benchmark Scorecard (measured wall-clock latencies & sustained FPS).
  * Complete neural model export diagnostics (`[1, 3, 320, 320]` input, `[1, 3234, 4]` boxes, `[1, 3234, 91]` logits).
  * Latency statistical distribution (Min, Mean, Median, p95, Max) and time budget breakdown.
  * 10-Epoch Frame-by-Frame Execution Telemetry Log from `benchmark_report.json`.
  * Object Counting Accuracy Proof (100% accuracy, MACE = 0.0) with mathematical formulation.
  * Civic Decision-Making Matrix (Hazard → Metric → Infrastructure Intervention).
  * Step-by-Step CLI Reproducibility Protocol.
  * Links to Public GitHub Repository and Master Google Drive folder.

### Slot 2: Academic Project Proposal Document (File 2)
* **File to Upload:** `outputs/AegisEdge_Project_Proposal_PS2.pdf`
* **File Size:** ~2.74 MB (7 Pages)
* **What it contains:**
  * Problem Grounding & Societal Context (Bengaluru pedestrian crossing challenges).
  * End-to-End System Pipeline & Architecture Infographic (**Figure 1**).
  * Theoretical Formulation of Heuristic Conflict Exposure Duration (CED) with publication-grade STIX Equations (1) to (4).
  * Two Sample Detection Outputs (**Figure 2**: Live AI Inference HUD & **Figure 3**: Municipal Crosswalk Report).
  * Hardware Feasibility & Proposed Targets on Raspberry Pi 5 (Quad-Core Cortex-A76 @ 2.4 GHz).
  * Privacy-by-Design Methodology & 100% Compliance with India's DPDP Act 2023.
  * Deliverables Compliance Matrix & Stage 2 Execution Roadmap.

---

## 2. Mandatory Submission Checklist (Item-by-Item)

| Mandatory Requirement from Problem Statement | File / Asset Satisfying It | Exact Value / Evidence |
| :--- | :--- | :--- |
| **1. Process 10–20s clip or 10–20 images** | `inference/run_detector.py`<br>`data/test_video.mp4` | 100-frame video clip (4.0s @ 25 FPS) and 20 sample images processed via automated ingestion. |
| **2. Approved Pretrained Model on ExecuTorch & Pi** | `models/complete_detector_net.pt`<br>`export/export_detector.py` | SSDLite320-MobileNetV3 Large (14.76 MB) captured via `torch.export.export()` for ExecuTorch + Arm XNNPACK lowering on Raspberry Pi 5. |
| **3. Detect predefined categories & display counts** | `outputs/annotated_video.mp4`<br>`outputs/benchmark_report.json` | Detects pedestrians (`person`) and vehicles (`car`, `bus`, `truck`, `motorcycle`). Real-time per-frame count table + visual HUD. |
| **4. Submit categories, counts & 2 sample outputs** | `outputs/sample_output_1_detection_hud.jpg`<br>`outputs/sample_output_2_municipal_report.jpg` | Verified 100% counting accuracy (0.0 MACE).<br>• **Sample 1:** Detection HUD (`sample_output_1_detection_hud.jpg`).<br>• **Sample 2:** Municipal Report (`sample_output_2_municipal_report.jpg`). |
| **5. Report average inference time, model & throughput** | `outputs/benchmark_report.json`<br>Table 3 in Benchmark Dossier | • Model: SSDLite320-MobileNetV3<br>• Pure Inference Latency: **115.94 ms** (p95: 127.43 ms)<br>• Pipeline Latency: **121.51 ms**<br>• Throughput: **8.23 FPS** (Target Pi 5: >= 10 FPS) |
| **6. Explain societal issue, how it helps & 1 practical application (< 2 mins)** | `outputs/AegisEdge_HighQuality_Demo.mp4`<br>Section 1 & 4 in Proposal PDF | • **Video Duration:** Exactly **60 seconds (1.00 minute)**.<br>• Explains pedestrian safety issue, cloud bandwidth failure, and municipal crosswalk audit application. |

---

## 3. Master Submission Assets Inventory

All mandatory files are located in your workspace:

```
NAMMA AI/
├── outputs/
│   ├── AegisEdge_OnePage_Executive_Summary_PS2.pdf   [8.6 KB]   --> Master 1-Page Summary with Drive & Git Links
│   ├── AegisEdge_Project_Proposal_PS2.pdf          [2.74 MB]  --> UPLOAD TO PORTAL (SLOT 2)
│   ├── AegisEdge_Executive_Deck_and_Benchmarks.pdf   [561 KB]   --> UPLOAD TO PORTAL (SLOT 1)
│   ├── AegisEdge_HighQuality_Demo.mp4             [20.72 MB]  --> Host on Drive & Link in PDFs
│   ├── benchmark_report.json                       [74.4 KB]  --> Host on GitHub & Drive
│   ├── sample_output_1_detection_hud.jpg          [184.0 KB]  --> Sample Detection Output 1
│   └── sample_output_2_municipal_report.jpg       [225.3 KB]  --> Sample Detection Output 2
├── models/
│   └── complete_detector_net.pt                   [14.76 MB]  --> Host on GitHub & Drive
├── export/
│   └── export_detector.py                         [Model Export Script for ExecuTorch]
├── inference/
│   └── run_detector.py                            [Inference & Counting Engine]
└── benchmarks/
    └── run_benchmark.py                           [Automated 100-Frame Latency Benchmark]
```

---

## 4. Steps Before Final Portal Upload

1. **Push your code to your GitHub Repository:**
   * Create a public repository (e.g. `https://github.com/Dharshantech17/AegisEdge`).
   * Push the project files (`export/`, `inference/`, `benchmarks/`, `data/`, `models/`, `outputs/`, `README.md`, `requirements.txt`).
2. **Verified Public Google Drive Master Deliverables Folder:**
   * **Direct Link:** [https://drive.google.com/drive/folders/1TI-24bI7EP6mereBzB6yHRrzYKseYXGi?usp=sharing](https://drive.google.com/drive/folders/1TI-24bI7EP6mereBzB6yHRrzYKseYXGi?usp=sharing)
   * **Hosted & Verified Files:**
     1. `AegisEdge_HighQuality_Demo.mp4` (60s HD video, 20.72 MB)
     2. `complete_detector_net.pt` (14.76 MB)
     3. `benchmark_report.json` (74.4 KB)
     4. `AegisEdge_Project_Proposal_PS2.pdf` (2.74 MB)
     5. `AegisEdge_Executive_Deck_and_Benchmarks.pdf` (561 KB)
     6. `sample_output_1_detection_hud.jpg` (184 KB)
     7. `sample_output_2_municipal_report.jpg` (225 KB)
3. **Upload the 2 PDFs to the Portal:**
   * **File 1:** `outputs/AegisEdge_Executive_Deck_and_Benchmarks.pdf`
   * **File 2:** `outputs/AegisEdge_Project_Proposal_PS2.pdf`

