from django.shortcuts import render

# Create your views here.

import cv2
import mediapipe as mp
from ultralytics import YOLO
import os
import tempfile
import logging
import mimetypes
import random
from django.conf import settings
from django.http import FileResponse
from django.core.files import File
from django.http import StreamingHttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import UploadedVideoSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class TimingAnalysisView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if 'video' not in request.FILES:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        video_file = request.FILES['video']
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            for chunk in video_file.chunks():
                temp_video.write(chunk)
            temp_video_path = temp_video.name
        
        logger.debug(f"Temporary video saved at: {temp_video_path}")

        try:
            # Process the video
            processed_video_path = self.process_video(temp_video_path)

            # Save the processed video to media/processed_video
            with open(processed_video_path, 'rb') as f:
                saved_path = default_storage.save('time_processed_video/processed_video.mp4', ContentFile(f.read()))
            
            # Get the full URL of the saved video
            video_url = request.build_absolute_uri(default_storage.url(saved_path))

            # Return the full URL of the processed video
            return Response({'video_url': video_url}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Clean up temporary files
            if os.path.exists(temp_video_path):
                os.unlink(temp_video_path)
            if 'processed_video_path' in locals() and os.path.exists(processed_video_path):
                os.unlink(processed_video_path)

    def process_video(self, video_path):
        # Initialize video capture
        cap = cv2.VideoCapture(video_path)
        frame_height, frame_width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # Create a temporary file for the output video
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

        # Initialize MediaPipe and YOLO
        mp_hands = mp.solutions.hands
        mp_pose = mp.solutions.pose
        hands = mp_hands.Hands()
        pose = mp_pose.Pose()
    
        # Use settings for model paths
        model = YOLO(settings.YOLO_MODEL_PATH)
        model2 = YOLO(settings.BAT_DETECTOR_MODEL_PATH)

        # Function to detect ball using YOLO
        def detect_ball(frame):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(rgb_frame)
            ball_center = None
        
            for result in results:
                detections = result.boxes.xyxy.cpu().numpy()  # bounding box coordinates
                classes = result.boxes.cls.cpu().numpy()  # class indices
                for i, (x1, y1, x2, y2) in enumerate(detections):
                    if classes[i] == 32:  # Assuming 'sports ball' class ID is 32
                        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                        ball_center = (cx, cy)
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                        break
        
                return ball_center

        # Function to detect bat using YOLO
        def detect_bat(frame):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model2(rgb_frame)
            bat_tip = None
        
            for result in results:
                detections = result.boxes.xyxy.cpu().numpy()  # bounding box coordinates
                classes = result.boxes.cls.cpu().numpy()  # class indices
                for i, (x1, y1, x2, y2) in enumerate(detections):
                    if classes[i] == 1:
                        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                        bat_tip = (cx, cy)
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)
                        break
        
            return bat_tip
    
        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                # Process the frame with MediaPipe Hands and Pose
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hand_results = hands.process(frame_rgb)
                pose_results = pose.process(frame_rgb)

                # Draw landmarks
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if pose_results.pose_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Detect ball and bat
                ball_position = detect_ball(frame)
                bat_position = detect_bat(frame)

                # Logic to determine hit timing and display text
                if bat_position and ball_position:
                    # Calculate the vertical thirds of the bat
                    bat_third_height = (bat_position[1] + frame_height // 3) // 3
                    lower_third = bat_position[1] + bat_third_height
                    upper_third = bat_position[1] + 2 * bat_third_height

                    # Determine where the ball hits the bat
                    if ball_position[1] < lower_third:
                        timing_text = "LATE"
                    elif ball_position[1] < upper_third:
                        timing_text = "ON TIME"
                    else:
                        timing_text = "EARLY"

                    # Reset the text frames counter
                    text_frames = 0
                    text_display_duration = 100

                    # Display the timing text in the center of the video screen in green color
                    if timing_text is not None and text_frames < text_display_duration:
                        font_scale = 5  # Increase the font scale
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_thickness = 10
                        text_size = cv2.getTextSize(timing_text, font, font_scale, font_thickness)[0]
                        text_x = (frame_width - text_size[0]) // 2
                        text_y = (frame_height + text_size[1]) // 2
                        cv2.putText(frame, timing_text, (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)
                        text_frames += 1

                # Write the frame to the output video
                out.write(frame)
        
        finally:
            # Ensure everything is properly closed
            cap.release()
            out.release()
            cv2.destroyAllWindows()

        return output_path

