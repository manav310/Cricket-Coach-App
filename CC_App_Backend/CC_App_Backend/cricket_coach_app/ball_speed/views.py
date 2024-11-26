import os
import tempfile
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid GUI issues
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from .models import BallSpeedVideo
from .serializers import BallSpeedVideoSerializer

class BallSpeedAnalysisView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if 'video' not in request.FILES:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        video_file = request.FILES['video']
        serializer = BallSpeedVideoSerializer(data={'video': video_file})

        if serializer.is_valid():
            video_instance = serializer.save()
            video_path = video_instance.video.path

            try:
                # Analyze the ball speed
                average_speed_kmh, speed_data = self.analyze_ball_speed(video_path)

                # Generate PDF with results
                pdf_path = self.generate_pdf(average_speed_kmh, speed_data)

                # Return PDF as response
                with open(pdf_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=ball_speed_analysis.pdf'
        
                # Clean up
                os.remove(pdf_path)
                os.remove(video_path)  # Remove the uploaded video file
                return response

            except Exception as e:
                # Make sure to clean up in case of an error
                if os.path.exists(video_path):
                    os.remove(video_path)
                if 'pdf_path' in locals() and os.path.exists(pdf_path):
                    os.remove(pdf_path)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def analyze_ball_speed(self, video_path):
        # Constants (you may need to adjust these based on your specific setup)
        person_height_meters = 1.6764  # Height of the person in meters

        # Load the YOLO models
        ballmodel_path = os.path.join(settings.BASE_DIR, '..', 'models', 'ball_detector', 'last.pt')
        ball_model = YOLO(ballmodel_path)
        personmodel_path = os.path.join(settings.BASE_DIR, '..', 'models', 'yolov8x.pt')
        person_model = YOLO(personmodel_path)

        # Load the video
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Detect person and calculate distance per pixel
        distance_per_pixel = self.calculate_distance_per_pixel(cap, person_model, person_height_meters)

        # Reload the video for ball tracking
        cap = cv2.VideoCapture(video_path)

        # Track the ball without saving the video
        results = ball_model.track(source=video_path, conf=0.1, save=False, stream=True)

        # Process results
        prev_center = None
        speeds = []
        frame_count = 0

        for result in results:
            if result.boxes.id is not None:
                boxes = result.boxes.xywh.cpu()
                for box in boxes:
                    x, y, w, h = box
                    current_center = np.array([x, y])

                    if prev_center is not None:
                        pixel_distance = np.linalg.norm(current_center - prev_center)
                        real_world_distance = pixel_distance * distance_per_pixel  # Convert to meters
                        time_between_frames = 1 / fps  # Time in seconds
                        speed_mps = real_world_distance / time_between_frames  # Speed in meters per second
                        speed_kmh = speed_mps * 3.6  # Convert m/s to km/h
                        speeds.append(speed_kmh)

                    prev_center = current_center
        
            frame_count += 1

        cap.release()

        if speeds:
            average_speed_kmh = np.mean(speeds)
        else:
            average_speed_kmh = 0

        return average_speed_kmh, speeds

    def calculate_distance_per_pixel(self, cap, person_model, person_height_meters):
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            results = person_model.predict(frame)

            for result in results:
                for box in result.boxes:
                    if box.cls == 0:  # Assuming class '0' is 'person' in COCO dataset
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        box_height_pixels = y2 - y1
                        distance_per_pixel = (person_height_meters / box_height_pixels) * 3.3
                        return distance_per_pixel  # This is now in meters per pixel

            raise ValueError("Person not detected in the video")

    def generate_pdf(self, average_speed_kmh, speed_data):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf_path = temp_pdf.name

        with PdfPages(pdf_path) as pdf:
            # Plot 1: Average Speed
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(['Average Ball Speed'], [average_speed_kmh])
            ax.set_ylabel('Speed (km/h)')
            ax.set_title('Average Ball Speed')
            pdf.savefig(fig)
            plt.close(fig)

            # Plot 2: Speed over time
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(len(speed_data)), speed_data)
            ax.set_xlabel('Frame')
            ax.set_ylabel('Speed (km/h)')
            ax.set_title('Ball Speed Over Time')
            pdf.savefig(fig)
            plt.close(fig)

        return pdf_path

# Note: This view now processes the video and returns a PDF response directly,
# similar to the body stance analysis approach. It includes the ball speed
# calculation logic from the original implementation.

