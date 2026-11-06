"""
Lightweight Centroid & IoU Edge Tracker for AegisEdge.
Designed for minimal CPU overhead (<0.5ms per frame) on Arm Cortex-A.
"""

import numpy as np


class SimpleTracker:
    def __init__(self, max_disappeared=15, iou_threshold=0.3):
        self.next_object_id = 1
        self.objects = {}       # object_id -> bbox [x1, y1, x2, y2]
        self.disappeared = {}   # object_id -> consecutive frames disappeared
        self.classes = {}       # object_id -> class_name
        self.max_disappeared = max_disappeared
        self.iou_threshold = iou_threshold

    @staticmethod
    def _compute_iou(box_a, box_b):
        xA = max(box_a[0], box_b[0])
        yA = max(box_a[1], box_b[1])
        xB = min(box_a[2], box_b[2])
        yB = min(box_a[3], box_b[3])

        inter_area = max(0, xB - xA) * max(0, yB - yA)
        box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
        box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
        union_area = float(box_a_area + box_b_area - inter_area)

        return inter_area / union_area if union_area > 0 else 0.0

    def update(self, detections):
        """
        Args:
            detections: List of dicts, each with 'bbox': [x1, y1, x2, y2], 'class': str, 'score': float
        Returns:
            tracked_objects: List of dicts with 'id', 'bbox', 'class', 'score'
        """
        if len(detections) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)
            return self._get_active_tracks()

        if len(self.objects) == 0:
            for det in detections:
                self._register(det['bbox'], det['class'])
            return self._get_active_tracks()

        # Match existing objects to detections via IoU
        object_ids = list(self.objects.keys())
        existing_boxes = [self.objects[i] for i in object_ids]

        iou_matrix = np.zeros((len(object_ids), len(detections)), dtype=np.float32)
        for i, obj_box in enumerate(existing_boxes):
            for j, det in enumerate(detections):
                iou_matrix[i, j] = self._compute_iou(obj_box, det['bbox'])

        matched_objects = set()
        matched_detections = set()

        if iou_matrix.size > 0:
            # Greedy matching based on highest IoU
            for _ in range(min(len(object_ids), len(detections))):
                idx = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
                if iou_matrix[idx] < self.iou_threshold:
                    break
                obj_idx, det_idx = idx
                matched_objects.add(obj_idx)
                matched_detections.add(det_idx)
                
                obj_id = object_ids[obj_idx]
                self.objects[obj_id] = detections[det_idx]['bbox']
                self.classes[obj_id] = detections[det_idx]['class']
                self.disappeared[obj_id] = 0
                
                iou_matrix[obj_idx, :] = -1.0
                iou_matrix[:, det_idx] = -1.0

        # Handle unmatched existing tracks
        for i, obj_id in enumerate(object_ids):
            if i not in matched_objects:
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)

        # Handle new detections
        for j, det in enumerate(detections):
            if j not in matched_detections:
                self._register(det['bbox'], det['class'])

        return self._get_active_tracks()

    def _register(self, bbox, class_name):
        self.objects[self.next_object_id] = bbox
        self.classes[self.next_object_id] = class_name
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def _deregister(self, obj_id):
        self.objects.pop(obj_id, None)
        self.disappeared.pop(obj_id, None)
        self.classes.pop(obj_id, None)

    def _get_active_tracks(self):
        active = []
        for obj_id, bbox in self.objects.items():
            active.append({
                'id': obj_id,
                'bbox': bbox,
                'class': self.classes.get(obj_id, 'unknown')
            })
        return active

