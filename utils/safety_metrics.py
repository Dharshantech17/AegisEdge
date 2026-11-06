"""
Conflict-Exposure & Pedestrian Mobility Analytics Engine for AegisEdge.
Quantifies:
1. Spatial-temporal co-occupancy in designated crosswalk conflict zones (CED & CER).
2. Pedestrian Waiting-Time Analytics (PWA) prior to crossing.
3. Directional movement classification (Northbound vs Southbound crossing).
"""

import math
import numpy as np


class ConflictExposureAnalytics:
    def __init__(self, hazard_zone_ratio=0.5, lateral_proximity_norm=0.35, debounce_gap_frames=6):
        """
        Args:
            hazard_zone_ratio: Fraction of lower frame representing active carriageway.
            lateral_proximity_norm: Normalized lateral distance (|x_p - x_v| / width)
                                    threshold for sharing the same crossing corridor.
            debounce_gap_frames: Maximum detection loss frames before closing an event.
        """
        self.hazard_zone_ratio = hazard_zone_ratio
        self.lateral_proximity_norm = lateral_proximity_norm
        self.debounce_gap_frames = debounce_gap_frames
        self.vehicle_classes = {'car', 'bus', 'truck', 'motorcycle', 'bicycle'}
        self.pedestrian_classes = {'person'}
        
        # Exposure tracking
        self.total_overlap_frames = 0
        self.total_conflict_events = 0
        self.is_currently_in_event = False
        self.frames_since_last_overlap = 999
        
        # Unique counts & persistent trajectories
        self.unique_pedestrians = set()
        self.unique_vehicles = set()
        self.pedestrian_trajectories = {}  # id -> list of (gx, gy, frame_id)
        self.pedestrian_wait_frames = {}   # id -> frames spent in waiting zone
        
        # Directional flow counts
        self.pedestrians_crossing_down = 0  # Curbside to Carriageway
        self.pedestrians_crossing_up = 0    # Carriageway to Curbside
        
        self.total_processed_frames = 0
        self.cumulative_video_time_sec = 0.0

    @staticmethod
    def _get_ground_contact_point(bbox):
        """
        Calculates bottom-center coordinate ((x1 + x2)/2, y2).
        Represents the physical contact point on the road surface.
        """
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2.0, y2)

    def analyze_frame(self, tracked_objects, frame_width, frame_height, source_fps=20.0):
        """
        Analyzes tracked objects for a single frame.
        Args:
            tracked_objects: List of dicts with 'id', 'bbox', 'class'
            frame_width, frame_height: Frame dimensions
            source_fps: Original video recording FPS (determines delta_t)
        Returns:
            telemetry: Dict containing counts, CED/CER metrics, and waiting-time statistics.
        """
        self.total_processed_frames += 1
        delta_t_video = 1.0 / max(1.0, float(source_fps))
        self.cumulative_video_time_sec += delta_t_video
        
        pedestrians_in_crossing = []
        vehicles_in_crossing = []
        pedestrians_in_waiting_zone = []
        
        current_ped_count = 0
        current_veh_count = 0

        hazard_y_threshold = frame_height * (1.0 - self.hazard_zone_ratio)

        for obj in tracked_objects:
            c_name = obj['class'].lower()
            obj_id = obj['id']
            bbox = obj['bbox']
            gx, gy = self._get_ground_contact_point(bbox)

            if c_name in self.pedestrian_classes:
                current_ped_count += 1
                self.unique_pedestrians.add(obj_id)
                
                # Update trajectory history
                if obj_id not in self.pedestrian_trajectories:
                    self.pedestrian_trajectories[obj_id] = []
                    self.pedestrian_wait_frames[obj_id] = 0
                self.pedestrian_trajectories[obj_id].append((gx, gy, self.total_processed_frames))

                # Check zone: Waiting Zone (Sidewalk) vs Conflict Zone (Carriageway)
                if gy < hazard_y_threshold:
                    pedestrians_in_waiting_zone.append(obj_id)
                    self.pedestrian_wait_frames[obj_id] += 1
                else:
                    pedestrians_in_crossing.append((obj, gx, gy))
                    # Check directional progression
                    history = self.pedestrian_trajectories[obj_id]
                    if len(history) >= 5:
                        start_y = history[0][1]
                        current_y = gy
                        if current_y - start_y > 25:
                            self.pedestrians_crossing_down += 1
                        elif start_y - current_y > 25:
                            self.pedestrians_crossing_up += 1

            elif c_name in self.vehicle_classes:
                current_veh_count += 1
                self.unique_vehicles.add(obj_id)
                if gy >= hazard_y_threshold:
                    vehicles_in_crossing.append((obj, gx, gy))

        # Check corridor-bounded simultaneous occupancy
        meaningful_co_occupancy = False
        if pedestrians_in_crossing and vehicles_in_crossing:
            for _, p_gx, _ in pedestrians_in_crossing:
                for _, v_gx, _ in vehicles_in_crossing:
                    lateral_dist_norm = abs(p_gx - v_gx) / float(frame_width)
                    if lateral_dist_norm <= self.lateral_proximity_norm:
                        meaningful_co_occupancy = True
                        break
                if meaningful_co_occupancy:
                    break

        # Event grouping with debounce filter
        if meaningful_co_occupancy:
            self.total_overlap_frames += 1
            self.frames_since_last_overlap = 0
            if not self.is_currently_in_event:
                self.total_conflict_events += 1
                self.is_currently_in_event = True
        else:
            self.frames_since_last_overlap += 1
            if self.frames_since_last_overlap > self.debounce_gap_frames:
                self.is_currently_in_event = False

        # Cumulative Conflict Exposure Duration: CED = sum(I * delta_t_video)
        ced_seconds = round(self.total_overlap_frames * delta_t_video, 2)
        
        # Conflict Event Rate: CER = (N_events / T_observation) * 60 (events per minute)
        cer_per_minute = round((self.total_conflict_events / max(0.01, self.cumulative_video_time_sec)) * 60.0, 2)

        # Pedestrian Waiting-Time Analytics (PWA)
        wait_times_sec = [frames * delta_t_video for frames in self.pedestrian_wait_frames.values() if frames > 0]
        mean_wait_sec = round(float(np.mean(wait_times_sec)), 1) if wait_times_sec else 0.0
        max_wait_sec = round(float(np.max(wait_times_sec)), 1) if wait_times_sec else 0.0

        telemetry = {
            # Frame-level counts
            "frame_pedestrian_count": current_ped_count,
            "frame_vehicle_count": current_veh_count,
            "pedestrians_in_conflict_zone": len(pedestrians_in_crossing),
            "vehicles_in_conflict_zone": len(vehicles_in_crossing),
            "pedestrians_waiting": len(pedestrians_in_waiting_zone),
            
            # Cumulative unique counts
            "cumulative_unique_pedestrians": len(self.unique_pedestrians),
            "cumulative_unique_vehicles": len(self.unique_vehicles),
            
            # Conflict-Exposure Analytics (CED & CER)
            "simultaneous_occupancy": meaningful_co_occupancy,
            "total_conflict_overlap_events": self.total_conflict_events,
            "conflict_exposure_duration_sec": ced_seconds,
            "conflict_event_rate_per_min": cer_per_minute,
            
            # Pedestrian Waiting-Time Analytics (PWA)
            "mean_pedestrian_wait_sec": mean_wait_sec,
            "max_pedestrian_wait_sec": max_wait_sec,
            "total_video_time_sec": round(self.cumulative_video_time_sec, 2)
        }

        return telemetry
