"""
ExecuTorch & XNNPACK Model Export Pipeline for AegisEdge.
Exports the complete neural network architecture (Backbone + Multiscale Detection Heads)
of SSDLite320-MobileNetV3 for Arm Cortex-A (Raspberry Pi 5) acceleration.
"""

import os
import sys
import time
import torch
import torchvision
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class CompleteSSDLiteNet(torch.nn.Module):
    """
    Wraps the complete SSDLite320 neural network:
    Backbone Feature Extractor + Multi-Scale Classification & Regression Heads.
    Produces raw box regressions and classification logits suitable for static graph export.
    """
    def __init__(self, full_model):
        super().__init__()
        self.backbone = full_model.backbone
        self.head = full_model.head

    def forward(self, x):
        # x: (1, 3, 320, 320)
        features = self.backbone(x)
        # SSDLite head expects a list of feature map tensors from the pyramid
        feature_list = list(features.values())
        head_outputs = self.head(feature_list)
        # Returns tuple of raw regression tensors and classification logits
        # across all pyramid feature levels
        return head_outputs["bbox_regression"], head_outputs["cls_logits"]


def export_pipeline():
    print("=" * 75)
    print("AegisEdge: Complete SSDLite Neural Network Export Pipeline")
    print("Target Architecture: Arm Cortex-A76 (Raspberry Pi 5) via XNNPACK")
    print("=" * 75)

    # 1. Load SSDLite320-MobileNetV3 Large architecture
    print("[1/4] Loading SSDLite320-MobileNetV3 Large (Backbone + Multi-Head Detector)...")
    weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
    try:
        full_model = ssdlite320_mobilenet_v3_large(weights=weights)
        print("      Loaded pretrained COCO weights successfully.")
    except Exception as e:
        print(f"      [Offline/Local fallback] Initializing architecture without remote weights: {e}")
        full_model = ssdlite320_mobilenet_v3_large(weights=None, weights_backbone=None)

    full_model.eval()

    # 2. Wrap complete detector network (Backbone + Classification & Box Heads)
    print("[2/4] Constructing CompleteSSDLiteNet wrapper (Backbone + Detection Heads)...")
    complete_net = CompleteSSDLiteNet(full_model)
    complete_net.eval()

    sample_input = (torch.randn(1, 3, 320, 320, dtype=torch.float32),)

    with torch.no_grad():
        raw_boxes, raw_scores = complete_net(*sample_input)
        print(f"      Raw Bounding Box Regression Shape : {raw_boxes.shape}")
        print(f"      Raw Classification Logits Shape   : {raw_scores.shape}")

    # 3. PyTorch 2.x Static Graph Capture
    print("[3/4] Capturing complete computation graph via torch.export.export...")
    exported_program = torch.export.export(complete_net, sample_input)
    pt_path = os.path.join(OUTPUT_DIR, "complete_detector_net.pt")
    torch.save(exported_program, pt_path)
    print(f"      Saved PyTorch ExportedProgram: {pt_path}")
    print(f"      File size: {os.path.getsize(pt_path) / (1024 * 1024):.2f} MB")

    # 4. Lowering to ExecuTorch with XnnpackPartitioner
    print("[4/4] Lowering to ExecuTorch with XnnpackPartitioner...")
    try:
        from executorch.exir import to_edge_transform_and_lower
        from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner

        edge_prog = to_edge_transform_and_lower(
            exported_program,
            partitioner=[XnnpackPartitioner()]
        )
        pte_path = os.path.join(OUTPUT_DIR, "complete_detector_xnnpack.pte")
        with open(pte_path, "wb") as f:
            f.write(edge_prog.buffer())
        print(f"      SUCCESS! ExecuTorch binary written: {pte_path}")
        print(f"      Size: {os.path.getsize(pte_path) / (1024 * 1024):.2f} MB")
    except ImportError:
        print("      [NOTE] ExecuTorch SDK not detected in this host environment.")
        print("      ExportedProgram saved. The exact lowering snippet for Raspberry Pi OS is:")
        print("      `edge_prog = to_edge_transform_and_lower(prog, partitioner=[XnnpackPartitioner()])`")

    # Save target category mapping
    labels_path = os.path.join(OUTPUT_DIR, "coco_labels.txt")
    coco_classes = weights.meta["categories"]
    with open(labels_path, "w") as f:
        for idx, cat in enumerate(coco_classes):
            f.write(f"{idx}:{cat}\n")
    print(f"      Saved Category Map ({len(coco_classes)} classes): {labels_path}")

    print("\n Complete Detector Export validation finished!")
    print("=" * 75)


if __name__ == "__main__":
    export_pipeline()
