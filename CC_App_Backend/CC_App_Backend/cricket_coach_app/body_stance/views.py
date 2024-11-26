from django.shortcuts import render

# Create your views here.

import os
import tempfile
import uuid
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import cv2
import mediapipe as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Function to calculate Euclidean distance
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to calculate angle between three points
def calculate_angle(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ab = b - a
    bc = c - b
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

# Function to analyze video and return data for plots
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    data = {
        'left_knee_angle': [],
        'right_knee_angle': [],
        'shoulder_width': [],
        'feet_distance': [],
        'head_x': [],
        'head_y': [],
        'head_to_foot_distance': [],
        'eyes_level_diff': [],
        'center_of_mass_x': [],
        'center_of_mass_y': []
    }
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    is_left_handed = False  # Update this based on the batsman's handedness
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Knee Angles
            left_knee_angle = calculate_angle(
                (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame_height)
            )
            right_knee_angle = calculate_angle(
                (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * frame_height)
            )
            data['left_knee_angle'].append(left_knee_angle)
            data['right_knee_angle'].append(right_knee_angle)
            
            # Shoulder Width
            shoulder_width = calculate_distance(
                (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_height)
            )
            data['shoulder_width'].append(shoulder_width)
            
            # Feet Distance
            feet_distance = calculate_distance(
                (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y * frame_height)
            )
            data['feet_distance'].append(feet_distance)
            
            # Head Position
            head_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x * frame_width
            head_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y * frame_height
            data['head_x'].append(head_x)
            data['head_y'].append(head_y)
            
            # Head to Front Foot Distance
            front_foot = mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value if is_left_handed else mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value
            head_to_foot_distance = abs(landmarks[mp_pose.PoseLandmark.NOSE.value].x - landmarks[front_foot].x) * frame_width
            data['head_to_foot_distance'].append(head_to_foot_distance)
            
            # Eyes Level Difference
            eyes_level_diff = abs(landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y - landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y) * frame_height
            data['eyes_level_diff'].append(eyes_level_diff)
            
            # Center of Mass
            keypoints = [
                (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame_height),
                (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * frame_width, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * frame_height)
            ]
            center_of_mass_x = np.mean([kp[0] for kp in keypoints])
            center_of_mass_y = np.mean([kp[1] for kp in keypoints])
            data['center_of_mass_x'].append(center_of_mass_x)
            data['center_of_mass_y'].append(center_of_mass_y)
    
    cap.release()
    return data

# Plot all graphs and save as PDF
def plot_and_save(data, pdf_path):
    with PdfPages(pdf_path) as pdf:
        fig, axs = plt.subplots(4, 2, figsize=(15, 20))
        
        axs[0, 0].plot(data['left_knee_angle'], label='Left Knee Angle')
        axs[0, 0].plot(data['right_knee_angle'], label='Right Knee Angle')
        axs[0, 0].set_title("Knee Angles Over Time")
        axs[0, 0].set_xlabel("Frame Number")
        axs[0, 0].set_ylabel("Knee Angle (degrees)")
        axs[0, 0].legend()
        
        axs[0, 1].plot(data['shoulder_width'], label='Shoulder Width')
        axs[0, 1].set_title("Shoulder Width Over Time")
        axs[0, 1].set_xlabel("Frame Number")
        axs[0, 1].set_ylabel("Shoulder Width (pixels)")
        axs[0, 1].legend()
        
        axs[1, 0].plot(data['feet_distance'], label='Feet Distance')
        axs[1, 0].set_title("Feet Distance Over Time")
        axs[1, 0].set_xlabel("Frame Number")
        axs[1, 0].set_ylabel("Feet Distance (pixels)")
        axs[1, 0].legend()
        
        axs[1, 1].plot(data['head_x'], label='Head X Position')
        axs[1, 1].plot(data['head_y'], label='Head Y Position')
        axs[1, 1].set_title("Head Position Over Time")
        axs[1, 1].set_xlabel("Frame Number")
        axs[1, 1].set_ylabel("Position (pixels)")
        axs[1, 1].legend()
        
        axs[2, 0].plot(data['head_to_foot_distance'], label='Head to Front Foot Distance')
        axs[2, 0].set_title("Head to Front Foot Distance Over Time")
        axs[2, 0].set_xlabel("Frame Number")
        axs[2, 0].set_ylabel("Distance (pixels)")
        axs[2, 0].legend()
        
        axs[2, 1].plot(data['eyes_level_diff'], label='Eyes Level Difference')
        axs[2, 1].set_title("Eyes Level Difference Over Time")
        axs[2, 1].set_xlabel("Frame Number")
        axs[2, 1].set_ylabel("Difference in Y-coordinates (pixels)")
        axs[2, 1].legend()
        
        axs[3, 0].plot(data['center_of_mass_x'], label='Center of Mass X')
        axs[3, 0].plot(data['center_of_mass_y'], label='Center of Mass Y')
        axs[3, 0].set_title("Center of Mass Over Time")
        axs[3, 0].set_xlabel("Frame Number")
        axs[3, 0].set_ylabel("Center of Mass Position (pixels)")
        axs[3, 0].legend()
        
        fig.delaxes(axs[3, 1])
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)  # Close the figure to free up memory

class VideoAnalysisView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if 'video' not in request.FILES:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        video_file = request.FILES['video']
        temp_video_path = None
        temp_pdf_path = None

        try:
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                for chunk in video_file.chunks():
                    temp_video.write(chunk)
                temp_video_path = temp_video.name

            # Process the video
            data = process_video(temp_video_path)

            # Create a temporary file for the PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                temp_pdf_path = temp_pdf.name

            # Plot and save the graphs
            plot_and_save(data, temp_pdf_path)

            # Generate a unique identifier for the PDF
            pdf_id = str(uuid.uuid4())

            # Create the media/docs directory if it doesn't exist
            docs_dir = os.path.join(settings.MEDIA_ROOT, 'docs')
            os.makedirs(docs_dir, exist_ok=True)

            # Save the PDF to the media/docs directory
            pdf_filename = f"{pdf_id}.pdf"
            pdf_path = os.path.join(docs_dir, pdf_filename)
            with open(temp_pdf_path, 'rb') as temp_pdf, open(pdf_path, 'wb') as final_pdf:
                final_pdf.write(temp_pdf.read())

            # Create a response with the PDF ID
            response_data = {
                'pdf_id': pdf_id,
                'message': 'Analysis completed successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Clean up temporary files
            if temp_video_path and os.path.exists(temp_video_path):
                try:
                    os.unlink(temp_video_path)
                except Exception as e:
                    print(f"Error deleting temporary video file: {e}")

            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    os.unlink(temp_pdf_path)
                except Exception as e:
                    print(f"Error deleting temporary PDF file: {e}")

class DownloadPDFView(APIView):
    def get(self, request, pdf_id):
        pdf_filename = f"{pdf_id}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'docs', pdf_filename)

        if not os.path.exists(pdf_path):
            return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)

        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=analysis_{pdf_id}.pdf'
            return response

class PreviousAnalysesView(APIView):
    def get(self, request):
        docs_dir = os.path.join(settings.MEDIA_ROOT, 'docs')
        analyses = []
        
        for filename in os.listdir(docs_dir):
            if filename.endswith('.pdf'):
                pdf_id = filename[:-4]  # Remove .pdf extension
                file_path = os.path.join(docs_dir, filename)
                file_stat = os.stat(file_path)
                analyses.append({
                    'pdf_id': pdf_id,
                    'date': file_stat.st_mtime,  # Use file modification time as analysis date
                })
        
        # Sort analyses by date, most recent first
        analyses.sort(key=lambda x: x['date'], reverse=True)
        
        return Response(analyses, status=status.HTTP_200_OK)


