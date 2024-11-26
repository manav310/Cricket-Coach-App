import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Constants
pitch_length_meters = 60.12
frame_width_meters = pitch_length_meters
frame_width_pixels = 1280

def calculate_distance_pixels(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def convert_pixels_to_meters(distance_pixels, frame_width_pixels, frame_width_meters):
    return (distance_pixels / frame_width_pixels) * frame_width_meters

def calculate_speed_mps(distance_meters, time_seconds):
    return distance_meters / time_seconds

def convert_speed_to_kmh(speed_mps):
    return speed_mps * 3.6

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    speeds = [[], []]
    batsmen_tracks = [[], []]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        current_detections = []
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1]),
                   int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]))
            current_detections.append(hip)

        for detection in current_detections:
            if len(batsmen_tracks) < 2:
                batsmen_tracks.append([detection])
            else:
                distances = [calculate_distance_pixels(detection, track[-1]) if track else float('inf') for track in batsmen_tracks]
                closest_track = np.argmin(distances)
                batsmen_tracks[closest_track].append(detection)

        for i, track in enumerate(batsmen_tracks[:2]):
            if len(track) > 1:
                current_position = track[-1]
                prev_position = track[-2]

                distance_pixels = calculate_distance_pixels(prev_position, current_position)
                distance_meters = convert_pixels_to_meters(distance_pixels, frame.shape[1], frame_width_meters)
                speed_mps = calculate_speed_mps(distance_meters, 1 / fps)
                speed_kmh = convert_speed_to_kmh(speed_mps)
                speeds[i].append(speed_kmh)

    cap.release()

    avg_speeds = []
    for i in range(2):
        if speeds[i]:
            avg_speed_kmh = np.mean(speeds[i])
            avg_speeds.append({
                "batsman": i+1,
                "average_speed": round(avg_speed_kmh, 2),
                "unit": "km/h"
            })

    return avg_speeds

