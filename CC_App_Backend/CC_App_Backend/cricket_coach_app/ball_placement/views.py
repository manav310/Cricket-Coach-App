from django.shortcuts import render

# Create your views here.

import cv2
import numpy as np
import os
import tempfile
import logging
from django.conf import settings
from django.http import FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from ultralytics import YOLO

logger = logging.getLogger(__name__)

class BallPlacementAnalysisView(APIView):
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
                saved_path = default_storage.save('ball_processed_video/ball_place_processed.mp4', ContentFile(f.read()))
            
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
        # Load the YOLOv5 model
        model_path = os.path.join(settings.BASE_DIR, '..', 'models', 'yolov5su.pt')
        model = YOLO(model_path)

        # Read the video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError('Could not open video file')

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Create a temporary file for the output video
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name

        # Output video writer
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        # Initialize background subtractor
        fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

        # Initialize variables for direction tracking
        prev_center = None
        direction = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Apply the background subtractor to get the foreground mask
            fgmask = fgbg.apply(frame)
            # Threshold the mask to get binary mask
            _, thresh = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)

            # Detect cricket ball in the frame
            results = model(frame)
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    if cls == 32:  # Assuming the cricket ball label is 32
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        bbox_width = x2 - x1
                        bbox_height = y2 - y1

                        # Check if the bounding box size is within the desired range
                        if 10 < bbox_width < 100 and 10 < bbox_height < 100:
                            # Check if the detected object is in the moving region
                            if np.sum(thresh[y1:y2, x1:x2]) > 0:
                                # Calculate center of the bounding box
                                center = ((x1 + x2) // 2, (y1 + y2) // 2)

                                # Draw bounding box and label on the frame
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, f'Cricket Ball: {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                                # Determine direction based on movement of center
                                if prev_center is not None:
                                    if center[0] < prev_center[0]:
                                        direction = 'Offside'
                                    elif center[0] > prev_center[0]:
                                        direction = 'Onside'
                                    else:
                                        direction = 'Straight'

                                    # Display direction on frame
                                    cv2.putText(frame, f'Direction: {direction}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                                # Update previous center
                                prev_center = center

            # Write the frame to the output video 
            out.write(frame)

        # Release resources
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        return output_path

