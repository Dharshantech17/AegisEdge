"""
Generates synthetic sample video and test frames for local testing of AegisEdge
prior to receiving organizer-provided clips.
"""

import os
import cv2
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def create_synthetic_test_data():
    print("[*] Generating synthetic test video and sample images in 'data/'...")
    width, height = 640, 360
    fps = 20
    duration_sec = 5
    total_frames = fps * duration_sec

    video_path = os.path.join(DATA_DIR, "sample_clip.mp4")
    writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Generate synthetic video simulating street crosswalk
    for i in range(total_frames):
        frame = np.full((height, width, 3), 40, dtype=np.uint8)

        # Draw road
        cv2.rectangle(frame, (0, 160), (width, height), (70, 70, 70), -1)
        # Draw crosswalk markings
        for x in range(50, width, 60):
            cv2.rectangle(frame, (x, 180), (x + 30, 240), (220, 220, 220), -1)

        # Moving pedestrian (circle/pill)
        ped_x = int(100 + (i * 3) % (width - 200))
        ped_y = int(190 + 10 * np.sin(i / 5.0))
        cv2.circle(frame, (ped_x, ped_y), 15, (0, 255, 0), -1)
        cv2.rectangle(frame, (ped_x - 10, ped_y + 15), (ped_x + 10, ped_y + 45), (0, 200, 0), -1)

        # Moving vehicle (rectangle: Orange in BGR = (0, 140, 255))
        veh_x = int((width - 50) - (i * 6) % width)
        veh_y = 240
        cv2.rectangle(frame, (veh_x, veh_y), (veh_x + 90, veh_y + 40), (0, 140, 255), -1)

        writer.write(frame)

        # Also save sample images
        if i % 15 == 0:
            img_path = os.path.join(DATA_DIR, f"sample_frame_{i:03d}.jpg")
            cv2.imwrite(img_path, frame)

    writer.release()
    print(f"[+] Created synthetic test video: {video_path}")
    print(f"[+] Created sample images in: {DATA_DIR}")


if __name__ == "__main__":
    create_synthetic_test_data()

