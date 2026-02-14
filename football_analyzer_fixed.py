


# """
# ULTIMATE v3.1 - REFEREE OCCLUSION FIX
# Critical fix: Players occluded by referee now tracked properly
# """

# import cv2
# import numpy as np
# from ultralytics import YOLO
# import supervision as sv
# from collections import defaultdict
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# from pathlib import Path
# import pickle
# from datetime import datetime
# import json
# import base64
# import threading
# from concurrent.futures import ThreadPoolExecutor
# import queue

# # Import modules
# from modules.view_transformer import ViewTransformer
# from modules.player_filter import PlayerFilter
# from modules.heatmap_generator import HeatmapGenerator
# from modules.injury_predictor import InjuryPredictor
# from modules.recovery_planner import RecoveryPlanner
# from modules.recovery_card_generator import RecoveryCardGenerator


# class FootballPerformanceAnalyzer:
#     """ULTIMATE: Beautiful UI + Referee occlusion fix"""
    
#     def __init__(self, 
#                  player_model_path="models/weights/best.pt",
#                  pitch_model_path="models/weights/pitch_keypoint_detector.pt",
#                  debug_mode=False):
        
#         print("🔄 Initializing ULTIMATE Football Analyzer v3.1...")
#         print("   🔧 REFEREE OCCLUSION FIX ENABLED")
        
#         # Configuration
#         self.debug_mode = debug_mode
#         if debug_mode:
#             print("   🐛 DEBUG MODE: Verbose annotations")
#         else:
#             print("   🎬 PRODUCTION MODE: Beautiful clean annotations")
        
#         # Thread safety
#         self._lock = threading.RLock()
        
#         # Storage
#         self.player_tracks = {}
#         self.player_stats = {}
#         self.player_images = {}
#         self.tracker = None
        
#         # Load models
#         self.player_detector = YOLO(player_model_path)
        
#         self.pitch_detector = None
#         if Path(pitch_model_path).exists():
#             try:
#                 self.pitch_detector = YOLO(pitch_model_path)
#                 print("   ✅ Pitch keypoint detector loaded")
#             except Exception as e:
#                 print(f"   ⚠️  Could not load pitch detector: {e}")
        
#         # Class IDs
#         self.BALL_ID = 0
#         self.GOALKEEPER_ID = 1
#         self.PLAYER_ID = 2
#         self.REFEREE_ID = 3
        
#         # Initialize modules
#         self.view_transformer = ViewTransformer(pitch_model_path)
#         self.player_filter = PlayerFilter(max_players=22)
#         self.heatmap_generator = HeatmapGenerator()
        
#         # ULTRA-AGGRESSIVE TRACKING
#         self.tracker = sv.ByteTrack(
#             track_thresh=0.05,        
#             track_buffer=360,         # 12 seconds
#             match_thresh=0.65,        
#             frame_rate=30
#         )
        
#         # Beautiful annotators
#         self.ellipse_annotator = sv.EllipseAnnotator(
#             color=sv.Color.from_hex('#00BFFF'),
#             thickness=3
#         )
#         self.label_annotator = sv.LabelAnnotator(
#             text_color=sv.Color.from_hex('#FFFFFF'),
#             text_thickness=2, 
#             text_scale=0.7,
#             text_padding=8
#         )
        
#         # Recovery modules
#         self.injury_predictor = InjuryPredictor()
#         self.recovery_planner = RecoveryPlanner()
#         self.recovery_card_generator = RecoveryCardGenerator()
        
#         # Video metadata
#         self.fps = 30
#         self.frame_width = 1920
#         self.frame_height = 1080
#         self.total_frames = 0
        
#         # Parallel processing
#         self.executor = ThreadPoolExecutor(max_workers=2)
        
#         # Create directories
#         for folder in ["debug_frames", "recovery_cards", "player_cards", "heatmaps"]:
#             Path(folder).mkdir(exist_ok=True)
        
#         print("✅ ULTIMATE Analyzer initialized!")
#         print("   🎨 Beautiful ellipse annotations")
#         print("   🔧 Track buffer: 360 frames (12 seconds)")
#         print("   🔧 ULTRA-aggressive: thresh=0.05, match=0.65")
#         print("   ✅ Referee occlusion handled properly!")
    
#     def _reset_tracking(self):
#         """Reset everything"""
#         with self._lock:
#             self.tracker = sv.ByteTrack(
#                 track_thresh=0.05,
#                 track_buffer=360,
#                 match_thresh=0.65,
#                 frame_rate=30
#             )
#             self.player_tracks.clear()
#             self.player_stats.clear()
#             self.player_images.clear()
#             self.player_filter = PlayerFilter(max_players=22)
    
#     def process_video(self, video_path, progress_callback=None, 
#                      frame_callback=None, use_stubs=True):
#         """Main processing with referee occlusion fix"""
#         with self._lock:
#             video_path = str(video_path)
#             stub_path = Path(video_path).with_suffix('.pkl')
            
#             # Load cache
#             if use_stubs and stub_path.exists():
#                 print(f"📦 Loading cache...")
#                 try:
#                     with open(stub_path, 'rb') as f:
#                         cached = pickle.load(f)
                        
#                         if cached.get('version') != '3.1':
#                             print("⚠️  Old cache, reprocessing...")
#                             stub_path.unlink()
#                             raise ValueError("Old version")
                        
#                         self.player_tracks = cached['tracks']
#                         self.fps = cached['fps']
#                         self.frame_width = cached['width']
#                         self.frame_height = cached['height']
#                         self.total_frames = cached.get('total_frames', 0)
                        
#                         if 'filter_scores' in cached:
#                             self.player_filter.player_quality_scores = cached['filter_scores']
                        
#                         print("✅ Loaded from cache!")
#                         self._extract_best_crops(video_path)
#                         self._calculate_statistics()
#                         return self.player_stats, self.player_images
#                 except Exception as e:
#                     print(f"⚠️  Cache error: {e}")
            
#             # Fresh processing
#             self._reset_tracking()
            
#             cap = cv2.VideoCapture(video_path)
#             if not cap.isOpened():
#                 raise ValueError(f"Cannot open: {video_path}")
            
#             self.fps = cap.get(cv2.CAP_PROP_FPS) or 30
#             self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#             self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#             self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
#             print(f"\n📹 Video: {self.frame_width}x{self.frame_height} @ {self.fps:.1f}fps")
#             print(f"📊 Frames: {self.total_frames}\n")
            
#             # Pitch detection
#             ret, first_frame = cap.read()
#             if ret and self.pitch_detector:
#                 print("🎯 Detecting pitch...")
#                 success = self.view_transformer.calculate_transform_matrix(first_frame)
#                 print(f"   {'✅' if success else '⚠️ '} Pitch {'calibrated' if success else 'using fallback'}")
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
#             CONF_THRESHOLD = 0.05
#             print(f"🏃 ULTRA-AGGRESSIVE tracking with referee handling...\n")
            
#             frame_idx = 0
#             stats = {
#                 'frames_with_players': 0, 
#                 'total_detections': 0,
#                 'referee_near_player': 0  # New stat
#             }
            
#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
                
#                 timestamp = frame_idx / self.fps
                
#                 try:
#                     annotated, det_count, ref_near = self._process_and_annotate_frame(
#                         frame, timestamp, frame_idx, CONF_THRESHOLD
#                     )
                    
#                     if det_count > 0:
#                         stats['frames_with_players'] += 1
#                         stats['total_detections'] += det_count
                    
#                     if ref_near:
#                         stats['referee_near_player'] += 1
                    
#                     # Stream frames
#                     if frame_callback and frame_idx % 5 == 0:
#                         try:
#                             frame_callback(annotated.copy())
#                         except Exception as e:
#                             print(f"⚠️  Frame callback error: {e}")
                            
#                 except Exception as e:
#                     print(f"⚠️  Frame {frame_idx}: {e}")
#                     if frame_callback and frame_idx % 5 == 0:
#                         try:
#                             frame_callback(frame)
#                         except:
#                             pass
                
#                 frame_idx += 1
                
#                 if progress_callback and frame_idx % 10 == 0:
#                     progress_callback(min(95, (frame_idx / self.total_frames) * 100))
                
#                 # Detailed logging
#                 if frame_idx % 100 == 0:
#                     avg_det = stats['total_detections'] / max(1, stats['frames_with_players'])
#                     active_tracks = len([t for t in self.player_tracks.values() 
#                                        if t['last_seen'] and abs(t['last_seen'] - timestamp) < 1.0])
#                     total_tracks = len(self.player_tracks)
#                     long_lived = len([t for t in self.player_tracks.values() if t['frame_count'] > 50])
#                     ref_pct = (stats['referee_near_player'] / frame_idx) * 100
                    
#                     print(f"   🎬 Frame {frame_idx:4d}/{self.total_frames} | "
#                           f"Det:{avg_det:4.1f} | Active:{active_tracks:2d} | "
#                           f"Total:{total_tracks:2d} | Long:{long_lived:2d} | "
#                           f"Ref-near:{ref_pct:4.1f}%")
            
#             cap.release()
            
#             print(f"\n📊 Summary:")
#             print(f"   Frames with players: {stats['frames_with_players']}/{self.total_frames}")
#             print(f"   Avg detections: {stats['total_detections']/max(1,frame_idx):.1f}")
#             print(f"   Referee near player: {stats['referee_near_player']} frames ({stats['referee_near_player']/max(1,frame_idx)*100:.1f}%)")
#             print(f"   Total tracks: {len(self.player_tracks)}")
            
#             # Track duration stats
#             duration_stats = {
#                 'very_short (<30)': len([t for t in self.player_tracks.values() if t['frame_count'] < 30]),
#                 'short (30-100)': len([t for t in self.player_tracks.values() if 30 <= t['frame_count'] < 100]),
#                 'medium (100-500)': len([t for t in self.player_tracks.values() if 100 <= t['frame_count'] < 500]),
#                 'long (500+)': len([t for t in self.player_tracks.values() if t['frame_count'] >= 500])
#             }
#             print(f"   Track durations: {duration_stats}")
            
#             # Save cache
#             if use_stubs:
#                 print("\n💾 Saving...")
#                 try:
#                     with open(stub_path, 'wb') as f:
#                         pickle.dump({
#                             'version': '3.1',
#                             'tracks': dict(self.player_tracks),
#                             'fps': self.fps,
#                             'width': self.frame_width,
#                             'height': self.frame_height,
#                             'total_frames': self.total_frames,
#                             'filter_scores': self.player_filter.player_quality_scores
#                         }, f)
#                     print(f"   ✅ Saved")
#                 except Exception as e:
#                     print(f"   ⚠️  {e}")
            
#             print("\n📸 Extracting crops...")
#             self._extract_best_crops(video_path)
            
#             print("📊 Computing stats...")
#             self._calculate_statistics()
            
#             valid = len([p for p in self.player_stats if self.player_stats[p]['total_frames'] > 30])
#             print(f"\n✅ Complete! {valid} valid players, {len(self.player_stats)} total tracks")
            
#             if progress_callback:
#                 progress_callback(100)
            
#             return self.player_stats, self.player_images
    
#     def _process_and_annotate_frame(self, frame, timestamp, frame_idx, conf_threshold=0.05):
#         """
#         CRITICAL FIX: Handle referee occlusion properly
#         """
#         with self._lock:
#             # Detect ALL classes
#             results = self.player_detector(frame, conf=conf_threshold, verbose=False)[0]
#             detections = sv.Detections.from_ultralytics(results)
            
#             # Separate detections by class
#             ball_detections = detections[detections.class_id == self.BALL_ID]
#             referee_detections = detections[detections.class_id == self.REFEREE_ID]
#             players_and_gk = detections[
#                 (detections.class_id == self.PLAYER_ID) | 
#                 (detections.class_id == self.GOALKEEPER_ID)
#             ]
            
#             detection_count = len(players_and_gk)
            
#             # === CRITICAL FIX: Referee handling ===
#             # Do NOT run NMS between players and referees!
#             # Only run NMS WITHIN players
#             if len(players_and_gk) > 0:
#                 # NMS only among players (NOT with referee)
#                 players_and_gk = players_and_gk.with_nms(threshold=0.5, class_agnostic=False)
            
#             # Check if referee is near any player
#             referee_near_player = False
#             if len(referee_detections) > 0 and len(players_and_gk) > 0:
#                 for ref_box in referee_detections.xyxy:
#                     for player_box in players_and_gk.xyxy:
#                         # Check overlap
#                         iou = self._calculate_iou(ref_box, player_box)
#                         if iou > 0.01:  # Any overlap
#                             referee_near_player = True
#                             break
            
#             # === CRITICAL: Keep player detections even if referee overlaps ===
#             # The key is: we DON'T filter out players that overlap with referee
#             # We send ALL player detections to the tracker
            
#             # Ball padding
#             if len(ball_detections) > 0:
#                 try:
#                     padded = ball_detections.xyxy.copy()
#                     padded[:, [0,1]] -= 10
#                     padded[:, [2,3]] += 10
#                     padded = np.clip(padded, [0, 0, 0, 0], 
#                                     [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
#                     ball_detections.xyxy = padded
#                 except:
#                     pass
            
#             # Update tracker with ONLY players (not referee)
#             tracked = self.tracker.update_with_detections(players_and_gk)
            
#             # Store data for ALL tracked players
#             if tracked.tracker_id is not None and len(tracked) > 0:
#                 self._update_tracking_data(frame, tracked, timestamp, frame_idx)
                
#                 # Update quality scores
#                 confidences = tracked.confidence if hasattr(tracked, 'confidence') else None
#                 self.player_filter.update_quality_scores(
#                     tracked.tracker_id, confidences,
#                     players_and_gk.class_id[:len(tracked)], frame_idx
#                 )
                
#                 # Filter for visualization
#                 tracked_for_display, filtered_ids = self.player_filter.filter_detections(
#                     tracked, tracked.tracker_id
#                 )
#             else:
#                 tracked_for_display = tracked
            
#             # ========== ANNOTATION ==========
#             annotated = frame.copy()
            
#             # Debug: show raw detections
#             if self.debug_mode:
#                 # Players: green
#                 if len(players_and_gk) > 0:
#                     for bbox in players_and_gk.xyxy:
#                         x1, y1, x2, y2 = map(int, bbox)
#                         cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 1)
                
#                 # Referee: yellow (so you can see when they overlap)
#                 if len(referee_detections) > 0:
#                     for bbox in referee_detections.xyxy:
#                         x1, y1, x2, y2 = map(int, bbox)
#                         cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 255), 2)
#                         cv2.putText(annotated, "REF", (x1, y1-5),
#                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            
#             # Beautiful ellipses for players
#             if tracked_for_display.tracker_id is not None and len(tracked_for_display) > 0:
#                 annotated = self.ellipse_annotator.annotate(
#                     scene=annotated,
#                     detections=tracked_for_display
#                 )
                
#                 # Clean labels
#                 for i, track_id in enumerate(tracked_for_display.tracker_id):
#                     bbox = tracked_for_display.xyxy[i]
#                     x1, y1, x2, y2 = map(int, bbox)
                    
#                     cx = int((x1 + x2) / 2)
#                     cy = y1
                    
#                     # Label
#                     if self.debug_mode:
#                         track = self.player_tracks.get(track_id)
#                         label = f"#{track_id}"
#                         if track:
#                             label += f"({track['frame_count']})"
#                     else:
#                         label = f"#{track_id}"
                    
#                     # Label background
#                     (text_width, text_height), baseline = cv2.getTextSize(
#                         label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
#                     )
                    
#                     cv2.rectangle(
#                         annotated,
#                         (cx - text_width // 2 - 6, cy - text_height - 10),
#                         (cx + text_width // 2 + 6, cy - 4),
#                         (0, 191, 255),
#                         -1
#                     )
                    
#                     cv2.putText(
#                         annotated, label,
#                         (cx - text_width // 2, cy - 8),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
#                     )
            
#             # Enhanced ball
#             if len(ball_detections) > 0:
#                 for bbox in ball_detections.xyxy:
#                     cx = int((bbox[0] + bbox[2]) / 2)
#                     cy = int((bbox[1] + bbox[3]) / 2)
                    
#                     cv2.circle(annotated, (cx, cy), 16, (0, 255, 255), 2)
#                     cv2.circle(annotated, (cx, cy), 11, (0, 215, 255), -1)
#                     cv2.circle(annotated, (cx, cy), 7, (255, 255, 255), -1)
#                     cv2.circle(annotated, (cx, cy), 3, (0, 255, 255), -1)
            
#             # Info overlay
#             total_tracked = len(tracked.tracker_id) if tracked.tracker_id is not None else 0
#             active_tracks = len([t for t in self.player_tracks.values() 
#                                if abs(t.get('last_seen', 0) - timestamp) < 1.0])
            
#             ref_indicator = " ⚠️REF" if referee_near_player else ""
#             info_text = f"Frame {frame_idx}/{self.total_frames} | Det:{detection_count} Track:{total_tracked} Active:{active_tracks}{ref_indicator}"
            
#             (text_width, text_height), baseline = cv2.getTextSize(
#                 info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
#             )
            
#             cv2.rectangle(
#                 annotated,
#                 (5, 5),
#                 (15 + text_width, 15 + text_height + baseline),
#                 (0, 0, 0),
#                 -1
#             )
            
#             cv2.putText(
#                 annotated, info_text, (10, 10 + text_height),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
#             )
            
#             return annotated, detection_count, referee_near_player
    
#     def _calculate_iou(self, box1, box2):
#         """Calculate IoU between two boxes"""
#         x1_min, y1_min, x1_max, y1_max = box1
#         x2_min, y2_min, x2_max, y2_max = box2
        
#         # Intersection
#         inter_x_min = max(x1_min, x2_min)
#         inter_y_min = max(y1_min, y2_min)
#         inter_x_max = min(x1_max, x2_max)
#         inter_y_max = min(y1_max, y2_max)
        
#         if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
#             return 0.0
        
#         inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        
#         # Union
#         box1_area = (x1_max - x1_min) * (y1_max - y1_min)
#         box2_area = (x2_max - x2_min) * (y2_max - y2_min)
#         union_area = box1_area + box2_area - inter_area
        
#         return inter_area / union_area if union_area > 0 else 0.0
    
#     def _get_default_track(self):
#         """Default track structure"""
#         return {
#             'positions_pixels': [],
#             'positions_meters': [],
#             'timestamps': [],
#             'speeds': [],
#             'accelerations': [],
#             'position': None,
#             'frame_count': 0,
#             'first_seen': None,
#             'last_seen': None,
#             'confidence_scores': [],
#             'bboxes': []
#         }
    
#     def _update_tracking_data(self, frame, detections, timestamp, frame_idx):
#         """Store data for ALL tracked players"""
#         with self._lock:
#             if detections.tracker_id is None:
#                 return
            
#             for i, track_id in enumerate(detections.tracker_id):
#                 bbox = detections.xyxy[i]
#                 cx = float((bbox[0] + bbox[2]) / 2)
#                 cy = float(bbox[3])
#                 confidence = float(detections.confidence[i]) if hasattr(detections, 'confidence') else 0.5
                
#                 if track_id not in self.player_tracks:
#                     self.player_tracks[track_id] = self._get_default_track()
#                     self.player_tracks[track_id]['first_seen'] = timestamp
                
#                 track = self.player_tracks[track_id]
                
#                 track['positions_pixels'].append([float(cx), float(cy)])
#                 track['timestamps'].append(float(timestamp))
#                 track['frame_count'] += 1
#                 track['last_seen'] = timestamp
#                 track['confidence_scores'].append(confidence)
#                 track['bboxes'].append(bbox.tolist())
                
#                 pos_meters = self.view_transformer.transform_point(
#                     cx, cy, self.frame_width, self.frame_height
#                 )
#                 track['positions_meters'].append([float(pos_meters[0]), float(pos_meters[1])])
                
#                 if len(track['positions_meters']) > 1:
#                     prev_pos = track['positions_meters'][-2]
#                     curr_pos = track['positions_meters'][-1]
#                     dist = np.hypot(curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])
#                     time_diff = timestamp - track['timestamps'][-2]
                    
#                     if time_diff > 0:
#                         speed_kmh = float((dist / time_diff) * 3.6)
#                         speed_kmh = min(speed_kmh, 40.0)
#                         track['speeds'].append(speed_kmh)
                        
#                         if len(track['speeds']) > 1:
#                             speed_diff = track['speeds'][-1] - track['speeds'][-2]
#                             accel = float(speed_diff / time_diff)
#                             track['accelerations'].append(accel)
                
#                 if track['positions_meters']:
#                     x_m, y_m = track['positions_meters'][-1]
#                     track['position'] = self.view_transformer.get_position_zone(x_m, y_m)
    
#     def _extract_best_crops(self, video_path):
#         """Extract player crops"""
#         with self._lock:
#             cap = cv2.VideoCapture(str(video_path))
            
#             best_frames = {}
#             for tid, track in self.player_tracks.items():
#                 if track['frame_count'] < 15:
#                     continue
#                 if track['confidence_scores']:
#                     best_idx = np.argmax(track['confidence_scores'])
#                     best_frames[tid] = int(track['timestamps'][best_idx] * self.fps)
#                 else:
#                     mid_idx = len(track['timestamps']) // 2
#                     best_frames[tid] = int(track['timestamps'][mid_idx] * self.fps)
            
#             frame_idx = 0
#             needed = set(best_frames.values())
            
#             while cap.isOpened() and needed:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
                
#                 if frame_idx in needed:
#                     results = self.player_detector(frame, conf=0.1, verbose=False)[0]
#                     dets = sv.Detections.from_ultralytics(results)
                    
#                     for tid, target_frame in list(best_frames.items()):
#                         if frame_idx == target_frame and tid not in self.player_images:
#                             track = self.player_tracks[tid]
                            
#                             if track['positions_pixels']:
#                                 target_time = frame_idx / self.fps
#                                 timestamps = np.array(track['timestamps'])
#                                 closest_idx = np.argmin(np.abs(timestamps - target_time))
#                                 target_pos = track['positions_pixels'][closest_idx]
                                
#                                 min_dist = float('inf')
#                                 best_bbox = None
                                
#                                 for bbox in dets.xyxy:
#                                     cx = (bbox[0] + bbox[2]) / 2
#                                     cy = bbox[3]
#                                     dist = np.hypot(cx - target_pos[0], cy - target_pos[1])
#                                     if dist < min_dist and dist < 200:
#                                         min_dist = dist
#                                         best_bbox = bbox
                                
#                                 if best_bbox is not None:
#                                     try:
#                                         x1, y1, x2, y2 = map(int, best_bbox)
#                                         x1, y1 = max(0, x1-20), max(0, y1-20)
#                                         x2 = min(frame.shape[1], x2+20)
#                                         y2 = min(frame.shape[0], y2+20)
                                        
#                                         crop = frame[y1:y2, x1:x2]
#                                         if crop.size > 0 and crop.shape[0] > 40 and crop.shape[1] > 20:
#                                             self.player_images[tid] = crop
#                                     except:
#                                         pass
                    
#                     needed.discard(frame_idx)
#                 frame_idx += 1
            
#             cap.release()
#             print(f"   ✅ Extracted {len(self.player_images)} crops")
    
#     def _calculate_statistics(self):
#         """Calculate stats"""
#         with self._lock:
#             self.player_stats = {}
            
#             for player_id, track in self.player_tracks.items():
#                 if len(track['positions_meters']) < 15:
#                     continue
                
#                 try:
#                     positions = np.array(track['positions_meters'])
#                     speeds = np.array(track['speeds']) if track['speeds'] else np.array([0.0])
#                     accel = np.array(track['accelerations']) if track['accelerations'] else np.array([0.0])
                    
#                     total_dist = sum(np.linalg.norm(positions[i] - positions[i-1]) 
#                                     for i in range(1, len(positions)))
                    
#                     if speeds.size > 0:
#                         high_intensity_count = np.sum(speeds > 15.0)
#                         sprint_count = np.sum(speeds > 20.0)
#                         max_speed = float(np.max(speeds))
#                         avg_speed = float(np.mean(speeds))
#                     else:
#                         high_intensity_count = sprint_count = 0
#                         max_speed = avg_speed = 0.0
                    
#                     if accel.size > 0:
#                         accel_count = int(np.sum(accel > 0.5))
#                         decel_count = int(np.sum(accel < -0.5))
#                     else:
#                         accel_count = decel_count = 0
                    
#                     zones = self.view_transformer.get_zone_percentages(positions)
#                     avg_x, avg_y = float(np.mean(positions[:, 0])), float(np.mean(positions[:, 1]))
#                     position = self.view_transformer.get_position_zone(avg_x, avg_y)
                    
#                     hi_dist = 0.0
#                     if len(speeds) > 0 and len(positions) > 1:
#                         for i in range(1, len(positions)):
#                             if i-1 < len(speeds) and speeds[i-1] > 15.0:
#                                 hi_dist += np.linalg.norm(positions[i] - positions[i-1])
                    
#                     self.player_stats[player_id] = {
#                         'total_distance_km': round(total_dist / 1000, 2),
#                         'high_intensity_distance_km': round(hi_dist / 1000, 2),
#                         'sprint_count': int(sprint_count),
#                         'accelerations': accel_count,
#                         'decelerations': decel_count,
#                         'max_speed': round(max_speed, 1),
#                         'avg_speed': round(avg_speed, 1),
#                         'position': position,
#                         'position_zone': zones,
#                         'total_frames': track['frame_count'],
#                         'first_seen': track.get('first_seen', 0),
#                         'last_seen': track.get('last_seen', 0),
#                         'duration_seconds': round(track.get('last_seen', 0) - track.get('first_seen', 0), 1),
#                         'avg_confidence': float(np.mean(track.get('confidence_scores', [0.5]))),
#                         'positions': positions.tolist()
#                     }
#                 except Exception as e:
#                     print(f"⚠️  Stats error {player_id}: {e}")
            
#             print(f"   ✅ Stats for {len(self.player_stats)} players")
    
#     # Keep existing visualization methods (same as before)
#     def generate_player_card(self, player_id):
#         """Generate player card"""
#         with self._lock:
#             if player_id not in self.player_stats:
#                 return None
            
#             stats = self.player_stats[player_id]
#             fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
#             if player_id in self.player_images:
#                 try:
#                     img = cv2.cvtColor(self.player_images[player_id], cv2.COLOR_BGR2RGB)
#                     ax1.imshow(img)
#                     ax1.axis('off')
#                     ax1.set_title(f"Player #{player_id}\n{stats.get('position', 'Unknown')}", 
#                                  fontsize=16, fontweight='bold', pad=20)
#                 except:
#                     ax1.text(0.5, 0.5, f"#{player_id}", ha='center', va='center', fontsize=24)
#                     ax1.axis('off')
#             else:
#                 ax1.text(0.5, 0.5, f"#{player_id}", ha='center', va='center', fontsize=24)
#                 ax1.axis('off')
            
#             ax2.axis('off')
#             stats_text = f"""
# PERFORMANCE METRICS

# Distance:          {stats['total_distance_km']:.2f} km
# High Intensity:    {stats['high_intensity_distance_km']:.2f} km
# Sprints:           {stats['sprint_count']}
# Accelerations:     {stats['accelerations']}
# Decelerations:     {stats['decelerations']}

# Max Speed:         {stats['max_speed']:.1f} km/h
# Avg Speed:         {stats['avg_speed']:.1f} km/h

# POSITION: {stats.get('position', 'Unknown')}

# Field Distribution:
#   Defensive:  {stats['position_zone']['defensive']:.1f}%
#   Middle:     {stats['position_zone']['middle']:.1f}%
#   Attacking:  {stats['position_zone']['attacking']:.1f}%

# Tracked: {stats['total_frames']} frames ({stats['duration_seconds']}s)
#             """
#             ax2.text(0.05, 0.95, stats_text, fontsize=12, family='monospace',
#                     verticalalignment='top', transform=ax2.transAxes)
            
#             plt.tight_layout(pad=2.0)
#             return fig
    
#     def generate_heatmap(self, player_id, bins=60):
#         """Generate heatmap"""
#         with self._lock:
#             if player_id not in self.player_stats:
#                 return None
            
#             positions = None
#             if player_id in self.player_tracks:
#                 positions = np.array(self.player_tracks[player_id]['positions_meters'])
#             elif 'positions' in self.player_stats[player_id]:
#                 positions = np.array(self.player_stats[player_id]['positions'])
            
#             if positions is None or len(positions) < 10:
#                 return None
            
#             return self.heatmap_generator.generate_heatmap(
#                 positions=positions,
#                 player_id=player_id,
#                 position_name=self.player_stats[player_id].get('position', 'Unknown'),
#                 bins=bins
#             )
    
#     def export_to_json(self, output_path="analysis_output.json"):
#         """Export to JSON"""
#         with self._lock:
#             data = {
#                 "metadata": {
#                     "export_date": datetime.now().isoformat(),
#                     "version": "3.1-referee-fix",
#                     "video_info": {
#                         "width": self.frame_width,
#                         "height": self.frame_height,
#                         "fps": self.fps,
#                         "frames": self.total_frames
#                     },
#                     "players": len(self.player_stats)
#                 },
#                 "players": {}
#             }
            
#             for pid, stats in self.player_stats.items():
#                 img_b64 = ""
#                 if pid in self.player_images:
#                     try:
#                         _, buf = cv2.imencode('.jpg', self.player_images[pid])
#                         img_b64 = base64.b64encode(buf).decode('utf-8')
#                     except:
#                         pass
                
#                 positions = []
#                 if pid in self.player_tracks and 'positions_meters' in self.player_tracks[pid]:
#                     positions = self.player_tracks[pid]['positions_meters']
#                 elif 'positions' in stats:
#                     positions = stats['positions']
                
#                 data["players"][str(pid)] = {
#                     "stats": {k: v for k, v in stats.items() if k != 'positions'},
#                     "positions": positions[:1000],
#                     "image_base64": img_b64
#                 }
            
#             with open(output_path, 'w') as f:
#                 json.dump(data, f, indent=2)
            
#             print(f"✅ Exported to {output_path}")
#             return data
    
#     def generate_recovery_plan(self, player_id):
#         """Generate recovery plan"""
#         with self._lock:
#             if player_id not in self.player_stats:
#                 return None
            
#             try:
#                 stats = self.player_stats[player_id].copy()
#                 stats['player_id'] = player_id
#                 stats['match_date'] = datetime.now().strftime('%Y-%m-%d')
                
#                 injury = self.injury_predictor.predict(stats)
#                 recovery = self.recovery_planner.generate_recovery_plan(stats, injury)
                
#                 output = f"recovery_cards/player_{player_id}_recovery.png"
#                 fig = self.recovery_card_generator.generate_card(recovery, output)
#                 report = self.recovery_card_generator.generate_simple_text_report(recovery)
                
#                 return {
#                     'player_id': player_id,
#                     'injury_prediction': injury,
#                     'recovery_plan': recovery,
#                     'recovery_card_figure': fig,
#                     'recovery_card_path': output,
#                     'text_report': report
#                 }
#             except Exception as e:
#                 print(f"⚠️  Recovery plan error: {e}")
#                 return None


"""
ULTIMATE v3.1 - REFEREE OCCLUSION FIX + Google Drive Model Loading
Critical fix: Players occluded by referee now tracked properly
Deployment-ready: Models loaded from Google Drive for Render deployment
"""

import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import pickle
from datetime import datetime
import json
import base64
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
import gdown
import os

# Import modules
from modules.view_transformer import ViewTransformer
from modules.player_filter import PlayerFilter
from modules.heatmap_generator import HeatmapGenerator
from modules.injury_predictor import InjuryPredictor
from modules.recovery_planner import RecoveryPlanner
from modules.recovery_card_generator import RecoveryCardGenerator


class ModelDownloader:
    """Download models from Google Drive on first run"""
    
    # Google Drive file IDs extracted from share links
    MODELS = {
        'player': {
            'gdrive_id': '1Ay483Zu2lrDohXAMAVgmhkegqe7Rpyfy',  # best.pt
            'local_path': 'models/weights/best.pt',
            'url': 'https://drive.google.com/uc?id=1Ay483Zu2lrDohXAMAVgmhkegqe7Rpyfy'
        },
        'pitch': {
            'gdrive_id': '1XMClOwSWLOaV5N8WyM6k0CA3Xh9445zh',  # pitch_keypoint_detector.pt
            'local_path': 'models/weights/pitch_keypoint_detector.pt',
            'url': 'https://drive.google.com/uc?id=1XMClOwSWLOaV5N8WyM6k0CA3Xh9445zh'
        },
        'pose': {
            'gdrive_id': '1G5KXHTfzZplZ_-dQwUaO3t044JhSg5FH',  # yolov8-pose.pt
            'local_path': 'models/weights/yolov8_pose.pt',
            'url': 'https://drive.google.com/uc?id=1G5KXHTfzZplZ_-dQwUaO3t044JhSg5FH'
        }
    }
    
    @staticmethod
    def download_model(model_name, force=False):
        """Download a specific model from Google Drive"""
        if model_name not in ModelDownloader.MODELS:
            raise ValueError(f"Unknown model: {model_name}. Available: {list(ModelDownloader.MODELS.keys())}")
        
        model_info = ModelDownloader.MODELS[model_name]
        local_path = model_info['local_path']
        
        # Check if already exists
        if Path(local_path).exists() and not force:
            print(f"✅ {model_name} model already exists: {local_path}")
            return local_path
        
        # Create directory
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 Downloading {model_name} model from Google Drive...")
        print(f"   Target: {local_path}")
        
        try:
            # Download using gdown
            gdown.download(model_info['url'], local_path, quiet=False)
            
            if Path(local_path).exists():
                file_size = Path(local_path).stat().st_size / (1024 * 1024)  # MB
                print(f"✅ Downloaded {model_name} model ({file_size:.1f} MB)")
                return local_path
            else:
                raise Exception("Download completed but file not found")
                
        except Exception as e:
            print(f"❌ Failed to download {model_name} model: {e}")
            print(f"   Please download manually from:")
            print(f"   {model_info['url']}")
            print(f"   And place at: {local_path}")
            raise
    
    @staticmethod
    def download_all_models(force=False):
        """Download all required models"""
        print("\n🔄 Checking/downloading models from Google Drive...")
        paths = {}
        
        for model_name in ['player', 'pitch', 'pose']:
            try:
                paths[model_name] = ModelDownloader.download_model(model_name, force)
            except Exception as e:
                print(f"⚠️  Warning: Could not download {model_name} model")
                paths[model_name] = None
        
        print("✅ Model check complete!\n")
        return paths


class FootballPerformanceAnalyzer:
    """ULTIMATE: Beautiful UI + Referee occlusion fix + Google Drive models"""
    
    def __init__(self, 
                 player_model_path="models/weights/best.pt",
                 pitch_model_path="models/weights/pitch_keypoint_detector.pt",
                 pose_model_path="models/weights/yolov8_pose.pt",
                 debug_mode=False,
                 auto_download=True):
        
        print("🔄 Initializing ULTIMATE Football Analyzer v3.1...")
        print("   🔧 REFEREE OCCLUSION FIX ENABLED")
        print("   ☁️  GOOGLE DRIVE MODEL LOADING ENABLED")
        
        # Auto-download models from Google Drive if needed
        if auto_download:
            model_paths = ModelDownloader.download_all_models()
            if model_paths.get('player'):
                player_model_path = model_paths['player']
            if model_paths.get('pitch'):
                pitch_model_path = model_paths['pitch']
            if model_paths.get('pose'):
                pose_model_path = model_paths['pose']
        
        # Configuration
        self.debug_mode = debug_mode
        if debug_mode:
            print("   🐛 DEBUG MODE: Verbose annotations")
        else:
            print("   🎬 PRODUCTION MODE: Beautiful clean annotations")
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Storage
        self.player_tracks = {}
        self.player_stats = {}
        self.player_images = {}
        self.tracker = None
        
        # Load models
        # LOCAL LOADING (uncomment for local development):
        # self.player_detector = YOLO("models/weights/best.pt")
        # self.pitch_detector = YOLO("models/weights/pitch_keypoint_detector.pt")
        # self.pose_detector = YOLO("models/weights/yolov8_pose.pt")
        
        # GOOGLE DRIVE LOADING (for deployment):
        print(f"   📦 Loading player detector from: {player_model_path}")
        self.player_detector = YOLO(player_model_path)
        
        self.pitch_detector = None
        if Path(pitch_model_path).exists():
            try:
                print(f"   📦 Loading pitch detector from: {pitch_model_path}")
                self.pitch_detector = YOLO(pitch_model_path)
                print("   ✅ Pitch keypoint detector loaded")
            except Exception as e:
                print(f"   ⚠️  Could not load pitch detector: {e}")
        
        self.pose_detector = None
        if Path(pose_model_path).exists():
            try:
                print(f"   📦 Loading pose detector from: {pose_model_path}")
                self.pose_detector = YOLO(pose_model_path)
                print("   ✅ YOLOv8 pose detector loaded")
            except Exception as e:
                print(f"   ⚠️  Could not load pose detector: {e}")
        
        # Class IDs
        self.BALL_ID = 0
        self.GOALKEEPER_ID = 1
        self.PLAYER_ID = 2
        self.REFEREE_ID = 3
        
        # Initialize modules
        self.view_transformer = ViewTransformer(pitch_model_path)
        self.player_filter = PlayerFilter(max_players=22)
        self.heatmap_generator = HeatmapGenerator()
        
        # ULTRA-AGGRESSIVE TRACKING
        self.tracker = sv.ByteTrack(
            track_thresh=0.05,        
            track_buffer=360,         # 12 seconds
            match_thresh=0.65,        
            frame_rate=30
        )
        
        # Beautiful annotators
        self.ellipse_annotator = sv.EllipseAnnotator(
            color=sv.Color.from_hex('#00BFFF'),
            thickness=3
        )
        self.label_annotator = sv.LabelAnnotator(
            text_color=sv.Color.from_hex('#FFFFFF'),
            text_thickness=2, 
            text_scale=0.7,
            text_padding=8
        )
        
        # Recovery modules
        self.injury_predictor = InjuryPredictor()
        self.recovery_planner = RecoveryPlanner()
        self.recovery_card_generator = RecoveryCardGenerator()
        
        # Video metadata
        self.fps = 30
        self.frame_width = 1920
        self.frame_height = 1080
        self.total_frames = 0
        
        # Parallel processing
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Create directories
        for folder in ["debug_frames", "recovery_cards", "player_cards", "heatmaps"]:
            Path(folder).mkdir(exist_ok=True)
        
        print("✅ ULTIMATE Analyzer initialized!")
        print("   🎨 Beautiful ellipse annotations")
        print("   🔧 Track buffer: 360 frames (12 seconds)")
        print("   🔧 ULTRA-aggressive: thresh=0.05, match=0.65")
        print("   ✅ Referee occlusion handled properly!")
        print("   ✅ Pose detection available!" if self.pose_detector else "   ⚠️  Pose detection not loaded")
    
    def _reset_tracking(self):
        """Reset everything"""
        with self._lock:
            self.tracker = sv.ByteTrack(
                track_thresh=0.05,
                track_buffer=360,
                match_thresh=0.65,
                frame_rate=30
            )
            self.player_tracks.clear()
            self.player_stats.clear()
            self.player_images.clear()
            self.player_filter = PlayerFilter(max_players=22)
    
    def process_video(self, video_path, progress_callback=None, 
                     frame_callback=None, use_stubs=True):
        """Main processing with referee occlusion fix"""
        with self._lock:
            video_path = str(video_path)
            stub_path = Path(video_path).with_suffix('.pkl')
            
            # Load cache
            if use_stubs and stub_path.exists():
                print(f"📦 Loading cache...")
                try:
                    with open(stub_path, 'rb') as f:
                        cached = pickle.load(f)
                        
                        if cached.get('version') != '3.1':
                            print("⚠️  Old cache, reprocessing...")
                            stub_path.unlink()
                            raise ValueError("Old version")
                        
                        self.player_tracks = cached['tracks']
                        self.fps = cached['fps']
                        self.frame_width = cached['width']
                        self.frame_height = cached['height']
                        self.total_frames = cached.get('total_frames', 0)
                        
                        if 'filter_scores' in cached:
                            self.player_filter.player_quality_scores = cached['filter_scores']
                        
                        print("✅ Loaded from cache!")
                        self._extract_best_crops(video_path)
                        self._calculate_statistics()
                        return self.player_stats, self.player_images
                except Exception as e:
                    print(f"⚠️  Cache error: {e}")
            
            # Fresh processing
            self._reset_tracking()
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Cannot open: {video_path}")
            
            self.fps = cap.get(cv2.CAP_PROP_FPS) or 30
            self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            print(f"\n📹 Video: {self.frame_width}x{self.frame_height} @ {self.fps:.1f}fps")
            print(f"📊 Frames: {self.total_frames}\n")
            
            # Pitch detection
            ret, first_frame = cap.read()
            if ret and self.pitch_detector:
                print("🎯 Detecting pitch...")
                success = self.view_transformer.calculate_transform_matrix(first_frame)
                print(f"   {'✅' if success else '⚠️ '} Pitch {'calibrated' if success else 'using fallback'}")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            CONF_THRESHOLD = 0.05
            print(f"🏃 ULTRA-AGGRESSIVE tracking with referee handling...\n")
            
            frame_idx = 0
            stats = {
                'frames_with_players': 0, 
                'total_detections': 0,
                'referee_near_player': 0  # New stat
            }
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                timestamp = frame_idx / self.fps
                
                try:
                    annotated, det_count, ref_near = self._process_and_annotate_frame(
                        frame, timestamp, frame_idx, CONF_THRESHOLD
                    )
                    
                    if det_count > 0:
                        stats['frames_with_players'] += 1
                        stats['total_detections'] += det_count
                    
                    if ref_near:
                        stats['referee_near_player'] += 1
                    
                    # Stream frames
                    if frame_callback and frame_idx % 5 == 0:
                        try:
                            frame_callback(annotated.copy())
                        except Exception as e:
                            print(f"⚠️  Frame callback error: {e}")
                            
                except Exception as e:
                    print(f"⚠️  Frame {frame_idx}: {e}")
                    if frame_callback and frame_idx % 5 == 0:
                        try:
                            frame_callback(frame)
                        except:
                            pass
                
                frame_idx += 1
                
                if progress_callback and frame_idx % 10 == 0:
                    progress_callback(min(95, (frame_idx / self.total_frames) * 100))
                
                # Detailed logging
                if frame_idx % 100 == 0:
                    avg_det = stats['total_detections'] / max(1, stats['frames_with_players'])
                    active_tracks = len([t for t in self.player_tracks.values() 
                                       if t['last_seen'] and abs(t['last_seen'] - timestamp) < 1.0])
                    total_tracks = len(self.player_tracks)
                    long_lived = len([t for t in self.player_tracks.values() if t['frame_count'] > 50])
                    ref_pct = (stats['referee_near_player'] / frame_idx) * 100
                    
                    print(f"   🎬 Frame {frame_idx:4d}/{self.total_frames} | "
                          f"Det:{avg_det:4.1f} | Active:{active_tracks:2d} | "
                          f"Total:{total_tracks:2d} | Long:{long_lived:2d} | "
                          f"Ref-near:{ref_pct:4.1f}%")
            
            cap.release()
            
            print(f"\n📊 Summary:")
            print(f"   Frames with players: {stats['frames_with_players']}/{self.total_frames}")
            print(f"   Avg detections: {stats['total_detections']/max(1,frame_idx):.1f}")
            print(f"   Referee near player: {stats['referee_near_player']} frames ({stats['referee_near_player']/max(1,frame_idx)*100:.1f}%)")
            print(f"   Total tracks: {len(self.player_tracks)}")
            
            # Track duration stats
            duration_stats = {
                'very_short (<30)': len([t for t in self.player_tracks.values() if t['frame_count'] < 30]),
                'short (30-100)': len([t for t in self.player_tracks.values() if 30 <= t['frame_count'] < 100]),
                'medium (100-500)': len([t for t in self.player_tracks.values() if 100 <= t['frame_count'] < 500]),
                'long (500+)': len([t for t in self.player_tracks.values() if t['frame_count'] >= 500])
            }
            print(f"   Track durations: {duration_stats}")
            
            # Save cache
            if use_stubs:
                print("\n💾 Saving...")
                try:
                    with open(stub_path, 'wb') as f:
                        pickle.dump({
                            'version': '3.1',
                            'tracks': dict(self.player_tracks),
                            'fps': self.fps,
                            'width': self.frame_width,
                            'height': self.frame_height,
                            'total_frames': self.total_frames,
                            'filter_scores': self.player_filter.player_quality_scores
                        }, f)
                    print(f"   ✅ Saved")
                except Exception as e:
                    print(f"   ⚠️  {e}")
            
            print("\n📸 Extracting crops...")
            self._extract_best_crops(video_path)
            
            print("📊 Computing stats...")
            self._calculate_statistics()
            
            valid = len([p for p in self.player_stats if self.player_stats[p]['total_frames'] > 30])
            print(f"\n✅ Complete! {valid} valid players, {len(self.player_stats)} total tracks")
            
            if progress_callback:
                progress_callback(100)
            
            return self.player_stats, self.player_images
    
    def _process_and_annotate_frame(self, frame, timestamp, frame_idx, conf_threshold=0.05):
        """
        CRITICAL FIX: Handle referee occlusion properly
        """
        with self._lock:
            # Detect ALL classes
            results = self.player_detector(frame, conf=conf_threshold, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(results)
            
            # Separate detections by class
            ball_detections = detections[detections.class_id == self.BALL_ID]
            referee_detections = detections[detections.class_id == self.REFEREE_ID]
            players_and_gk = detections[
                (detections.class_id == self.PLAYER_ID) | 
                (detections.class_id == self.GOALKEEPER_ID)
            ]
            
            detection_count = len(players_and_gk)
            
            # === CRITICAL FIX: Referee handling ===
            # Do NOT run NMS between players and referees!
            # Only run NMS WITHIN players
            if len(players_and_gk) > 0:
                # NMS only among players (NOT with referee)
                players_and_gk = players_and_gk.with_nms(threshold=0.5, class_agnostic=False)
            
            # Check if referee is near any player
            referee_near_player = False
            if len(referee_detections) > 0 and len(players_and_gk) > 0:
                for ref_box in referee_detections.xyxy:
                    for player_box in players_and_gk.xyxy:
                        # Check overlap
                        iou = self._calculate_iou(ref_box, player_box)
                        if iou > 0.01:  # Any overlap
                            referee_near_player = True
                            break
            
            # === CRITICAL: Keep player detections even if referee overlaps ===
            # The key is: we DON'T filter out players that overlap with referee
            # We send ALL player detections to the tracker
            
            # Ball padding
            if len(ball_detections) > 0:
                try:
                    padded = ball_detections.xyxy.copy()
                    padded[:, [0,1]] -= 10
                    padded[:, [2,3]] += 10
                    padded = np.clip(padded, [0, 0, 0, 0], 
                                    [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    ball_detections.xyxy = padded
                except:
                    pass
            
            # Update tracker with ONLY players (not referee)
            tracked = self.tracker.update_with_detections(players_and_gk)
            
            # Store data for ALL tracked players
            if tracked.tracker_id is not None and len(tracked) > 0:
                self._update_tracking_data(frame, tracked, timestamp, frame_idx)
                
                # Update quality scores
                confidences = tracked.confidence if hasattr(tracked, 'confidence') else None
                self.player_filter.update_quality_scores(
                    tracked.tracker_id, confidences,
                    players_and_gk.class_id[:len(tracked)], frame_idx
                )
                
                # Filter for visualization
                tracked_for_display, filtered_ids = self.player_filter.filter_detections(
                    tracked, tracked.tracker_id
                )
            else:
                tracked_for_display = tracked
            
            # ========== ANNOTATION ==========
            annotated = frame.copy()
            
            # Debug: show raw detections
            if self.debug_mode:
                # Players: green
                if len(players_and_gk) > 0:
                    for bbox in players_and_gk.xyxy:
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 1)
                
                # Referee: yellow (so you can see when they overlap)
                if len(referee_detections) > 0:
                    for bbox in referee_detections.xyxy:
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 255), 2)
                        cv2.putText(annotated, "REF", (x1, y1-5),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            
            # Beautiful ellipses for players
            if tracked_for_display.tracker_id is not None and len(tracked_for_display) > 0:
                annotated = self.ellipse_annotator.annotate(
                    scene=annotated,
                    detections=tracked_for_display
                )
                
                # Clean labels
                for i, track_id in enumerate(tracked_for_display.tracker_id):
                    bbox = tracked_for_display.xyxy[i]
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    cx = int((x1 + x2) / 2)
                    cy = y1
                    
                    # Label
                    if self.debug_mode:
                        track = self.player_tracks.get(track_id)
                        label = f"#{track_id}"
                        if track:
                            label += f"({track['frame_count']})"
                    else:
                        label = f"#{track_id}"
                    
                    # Label background
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                    )
                    
                    cv2.rectangle(
                        annotated,
                        (cx - text_width // 2 - 6, cy - text_height - 10),
                        (cx + text_width // 2 + 6, cy - 4),
                        (0, 191, 255),
                        -1
                    )
                    
                    cv2.putText(
                        annotated, label,
                        (cx - text_width // 2, cy - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
                    )
            
            # Enhanced ball
            if len(ball_detections) > 0:
                for bbox in ball_detections.xyxy:
                    cx = int((bbox[0] + bbox[2]) / 2)
                    cy = int((bbox[1] + bbox[3]) / 2)
                    
                    cv2.circle(annotated, (cx, cy), 16, (0, 255, 255), 2)
                    cv2.circle(annotated, (cx, cy), 11, (0, 215, 255), -1)
                    cv2.circle(annotated, (cx, cy), 7, (255, 255, 255), -1)
                    cv2.circle(annotated, (cx, cy), 3, (0, 255, 255), -1)
            
            # Info overlay
            total_tracked = len(tracked.tracker_id) if tracked.tracker_id is not None else 0
            active_tracks = len([t for t in self.player_tracks.values() 
                               if abs(t.get('last_seen', 0) - timestamp) < 1.0])
            
            ref_indicator = " ⚠️REF" if referee_near_player else ""
            info_text = f"Frame {frame_idx}/{self.total_frames} | Det:{detection_count} Track:{total_tracked} Active:{active_tracks}{ref_indicator}"
            
            (text_width, text_height), baseline = cv2.getTextSize(
                info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            
            cv2.rectangle(
                annotated,
                (5, 5),
                (15 + text_width, 15 + text_height + baseline),
                (0, 0, 0),
                -1
            )
            
            cv2.putText(
                annotated, info_text, (10, 10 + text_height),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )
            
            return annotated, detection_count, referee_near_player
    
    def _calculate_iou(self, box1, box2):
        """Calculate IoU between two boxes"""
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # Intersection
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        
        if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
            return 0.0
        
        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        
        # Union
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0
    
    def _get_default_track(self):
        """Default track structure"""
        return {
            'positions_pixels': [],
            'positions_meters': [],
            'timestamps': [],
            'speeds': [],
            'accelerations': [],
            'position': None,
            'frame_count': 0,
            'first_seen': None,
            'last_seen': None,
            'confidence_scores': [],
            'bboxes': []
        }
    
    def _update_tracking_data(self, frame, detections, timestamp, frame_idx):
        """Store data for ALL tracked players"""
        with self._lock:
            if detections.tracker_id is None:
                return
            
            for i, track_id in enumerate(detections.tracker_id):
                bbox = detections.xyxy[i]
                cx = float((bbox[0] + bbox[2]) / 2)
                cy = float(bbox[3])
                confidence = float(detections.confidence[i]) if hasattr(detections, 'confidence') else 0.5
                
                if track_id not in self.player_tracks:
                    self.player_tracks[track_id] = self._get_default_track()
                    self.player_tracks[track_id]['first_seen'] = timestamp
                
                track = self.player_tracks[track_id]
                
                track['positions_pixels'].append([float(cx), float(cy)])
                track['timestamps'].append(float(timestamp))
                track['frame_count'] += 1
                track['last_seen'] = timestamp
                track['confidence_scores'].append(confidence)
                track['bboxes'].append(bbox.tolist())
                
                pos_meters = self.view_transformer.transform_point(
                    cx, cy, self.frame_width, self.frame_height
                )
                track['positions_meters'].append([float(pos_meters[0]), float(pos_meters[1])])
                
                if len(track['positions_meters']) > 1:
                    prev_pos = track['positions_meters'][-2]
                    curr_pos = track['positions_meters'][-1]
                    dist = np.hypot(curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])
                    time_diff = timestamp - track['timestamps'][-2]
                    
                    if time_diff > 0:
                        speed_kmh = float((dist / time_diff) * 3.6)
                        speed_kmh = min(speed_kmh, 40.0)
                        track['speeds'].append(speed_kmh)
                        
                        if len(track['speeds']) > 1:
                            speed_diff = track['speeds'][-1] - track['speeds'][-2]
                            accel = float(speed_diff / time_diff)
                            track['accelerations'].append(accel)
                
                if track['positions_meters']:
                    x_m, y_m = track['positions_meters'][-1]
                    track['position'] = self.view_transformer.get_position_zone(x_m, y_m)
    
    def _extract_best_crops(self, video_path):
        """Extract player crops"""
        with self._lock:
            cap = cv2.VideoCapture(str(video_path))
            
            best_frames = {}
            for tid, track in self.player_tracks.items():
                if track['frame_count'] < 15:
                    continue
                if track['confidence_scores']:
                    best_idx = np.argmax(track['confidence_scores'])
                    best_frames[tid] = int(track['timestamps'][best_idx] * self.fps)
                else:
                    mid_idx = len(track['timestamps']) // 2
                    best_frames[tid] = int(track['timestamps'][mid_idx] * self.fps)
            
            frame_idx = 0
            needed = set(best_frames.values())
            
            while cap.isOpened() and needed:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx in needed:
                    results = self.player_detector(frame, conf=0.1, verbose=False)[0]
                    dets = sv.Detections.from_ultralytics(results)
                    
                    for tid, target_frame in list(best_frames.items()):
                        if frame_idx == target_frame and tid not in self.player_images:
                            track = self.player_tracks[tid]
                            
                            if track['positions_pixels']:
                                target_time = frame_idx / self.fps
                                timestamps = np.array(track['timestamps'])
                                closest_idx = np.argmin(np.abs(timestamps - target_time))
                                target_pos = track['positions_pixels'][closest_idx]
                                
                                min_dist = float('inf')
                                best_bbox = None
                                
                                for bbox in dets.xyxy:
                                    cx = (bbox[0] + bbox[2]) / 2
                                    cy = bbox[3]
                                    dist = np.hypot(cx - target_pos[0], cy - target_pos[1])
                                    if dist < min_dist and dist < 200:
                                        min_dist = dist
                                        best_bbox = bbox
                                
                                if best_bbox is not None:
                                    try:
                                        x1, y1, x2, y2 = map(int, best_bbox)
                                        x1, y1 = max(0, x1-20), max(0, y1-20)
                                        x2 = min(frame.shape[1], x2+20)
                                        y2 = min(frame.shape[0], y2+20)
                                        
                                        crop = frame[y1:y2, x1:x2]
                                        if crop.size > 0 and crop.shape[0] > 40 and crop.shape[1] > 20:
                                            self.player_images[tid] = crop
                                    except:
                                        pass
                    
                    needed.discard(frame_idx)
                frame_idx += 1
            
            cap.release()
            print(f"   ✅ Extracted {len(self.player_images)} crops")
    
    def _calculate_statistics(self):
        """Calculate stats"""
        with self._lock:
            self.player_stats = {}
            
            for player_id, track in self.player_tracks.items():
                if len(track['positions_meters']) < 15:
                    continue
                
                try:
                    positions = np.array(track['positions_meters'])
                    speeds = np.array(track['speeds']) if track['speeds'] else np.array([0.0])
                    accel = np.array(track['accelerations']) if track['accelerations'] else np.array([0.0])
                    
                    total_dist = sum(np.linalg.norm(positions[i] - positions[i-1]) 
                                    for i in range(1, len(positions)))
                    
                    if speeds.size > 0:
                        high_intensity_count = np.sum(speeds > 15.0)
                        sprint_count = np.sum(speeds > 20.0)
                        max_speed = float(np.max(speeds))
                        avg_speed = float(np.mean(speeds))
                    else:
                        high_intensity_count = sprint_count = 0
                        max_speed = avg_speed = 0.0
                    
                    if accel.size > 0:
                        accel_count = int(np.sum(accel > 0.5))
                        decel_count = int(np.sum(accel < -0.5))
                    else:
                        accel_count = decel_count = 0
                    
                    zones = self.view_transformer.get_zone_percentages(positions)
                    avg_x, avg_y = float(np.mean(positions[:, 0])), float(np.mean(positions[:, 1]))
                    position = self.view_transformer.get_position_zone(avg_x, avg_y)
                    
                    hi_dist = 0.0
                    if len(speeds) > 0 and len(positions) > 1:
                        for i in range(1, len(positions)):
                            if i-1 < len(speeds) and speeds[i-1] > 15.0:
                                hi_dist += np.linalg.norm(positions[i] - positions[i-1])
                    
                    self.player_stats[player_id] = {
                        'total_distance_km': round(total_dist / 1000, 2),
                        'high_intensity_distance_km': round(hi_dist / 1000, 2),
                        'sprint_count': int(sprint_count),
                        'accelerations': accel_count,
                        'decelerations': decel_count,
                        'max_speed': round(max_speed, 1),
                        'avg_speed': round(avg_speed, 1),
                        'position': position,
                        'position_zone': zones,
                        'total_frames': track['frame_count'],
                        'first_seen': track.get('first_seen', 0),
                        'last_seen': track.get('last_seen', 0),
                        'duration_seconds': round(track.get('last_seen', 0) - track.get('first_seen', 0), 1),
                        'avg_confidence': float(np.mean(track.get('confidence_scores', [0.5]))),
                        'positions': positions.tolist()
                    }
                except Exception as e:
                    print(f"⚠️  Stats error {player_id}: {e}")
            
            print(f"   ✅ Stats for {len(self.player_stats)} players")
    
    # Keep existing visualization methods (same as before)
    def generate_player_card(self, player_id):
        """Generate player card"""
        with self._lock:
            if player_id not in self.player_stats:
                return None
            
            stats = self.player_stats[player_id]
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            if player_id in self.player_images:
                try:
                    img = cv2.cvtColor(self.player_images[player_id], cv2.COLOR_BGR2RGB)
                    ax1.imshow(img)
                    ax1.axis('off')
                    ax1.set_title(f"Player #{player_id}\n{stats.get('position', 'Unknown')}", 
                                 fontsize=16, fontweight='bold', pad=20)
                except:
                    ax1.text(0.5, 0.5, f"#{player_id}", ha='center', va='center', fontsize=24)
                    ax1.axis('off')
            else:
                ax1.text(0.5, 0.5, f"#{player_id}", ha='center', va='center', fontsize=24)
                ax1.axis('off')
            
            ax2.axis('off')
            stats_text = f"""
PERFORMANCE METRICS

Distance:          {stats['total_distance_km']:.2f} km
High Intensity:    {stats['high_intensity_distance_km']:.2f} km
Sprints:           {stats['sprint_count']}
Accelerations:     {stats['accelerations']}
Decelerations:     {stats['decelerations']}

Max Speed:         {stats['max_speed']:.1f} km/h
Avg Speed:         {stats['avg_speed']:.1f} km/h

POSITION: {stats.get('position', 'Unknown')}

Field Distribution:
  Defensive:  {stats['position_zone']['defensive']:.1f}%
  Middle:     {stats['position_zone']['middle']:.1f}%
  Attacking:  {stats['position_zone']['attacking']:.1f}%

Tracked: {stats['total_frames']} frames ({stats['duration_seconds']}s)
            """
            ax2.text(0.05, 0.95, stats_text, fontsize=12, family='monospace',
                    verticalalignment='top', transform=ax2.transAxes)
            
            plt.tight_layout(pad=2.0)
            return fig
    
    def generate_heatmap(self, player_id, bins=60):
        """Generate heatmap"""
        with self._lock:
            if player_id not in self.player_stats:
                return None
            
            positions = None
            if player_id in self.player_tracks:
                positions = np.array(self.player_tracks[player_id]['positions_meters'])
            elif 'positions' in self.player_stats[player_id]:
                positions = np.array(self.player_stats[player_id]['positions'])
            
            if positions is None or len(positions) < 10:
                return None
            
            return self.heatmap_generator.generate_heatmap(
                positions=positions,
                player_id=player_id,
                position_name=self.player_stats[player_id].get('position', 'Unknown'),
                bins=bins
            )
    
    def export_to_json(self, output_path="analysis_output.json"):
        """Export to JSON"""
        with self._lock:
            data = {
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "version": "3.1-referee-fix-gdrive",
                    "video_info": {
                        "width": self.frame_width,
                        "height": self.frame_height,
                        "fps": self.fps,
                        "frames": self.total_frames
                    },
                    "players": len(self.player_stats)
                },
                "players": {}
            }
            
            for pid, stats in self.player_stats.items():
                img_b64 = ""
                if pid in self.player_images:
                    try:
                        _, buf = cv2.imencode('.jpg', self.player_images[pid])
                        img_b64 = base64.b64encode(buf).decode('utf-8')
                    except:
                        pass
                
                positions = []
                if pid in self.player_tracks and 'positions_meters' in self.player_tracks[pid]:
                    positions = self.player_tracks[pid]['positions_meters']
                elif 'positions' in stats:
                    positions = stats['positions']
                
                data["players"][str(pid)] = {
                    "stats": {k: v for k, v in stats.items() if k != 'positions'},
                    "positions": positions[:1000],
                    "image_base64": img_b64
                }
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Exported to {output_path}")
            return data
    
    def generate_recovery_plan(self, player_id):
        """Generate recovery plan"""
        with self._lock:
            if player_id not in self.player_stats:
                return None
            
            try:
                stats = self.player_stats[player_id].copy()
                stats['player_id'] = player_id
                stats['match_date'] = datetime.now().strftime('%Y-%m-%d')
                
                injury = self.injury_predictor.predict(stats)
                recovery = self.recovery_planner.generate_recovery_plan(stats, injury)
                
                output = f"recovery_cards/player_{player_id}_recovery.png"
                fig = self.recovery_card_generator.generate_card(recovery, output)
                report = self.recovery_card_generator.generate_simple_text_report(recovery)
                
                return {
                    'player_id': player_id,
                    'injury_prediction': injury,
                    'recovery_plan': recovery,
                    'recovery_card_figure': fig,
                    'recovery_card_path': output,
                    'text_report': report
                }
            except Exception as e:
                print(f"⚠️  Recovery plan error: {e}")
                return None