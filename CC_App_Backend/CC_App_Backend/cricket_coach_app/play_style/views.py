from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import analyze_video
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class AnalyzePlayStyleView(APIView):
    def post(self, request):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the video temporarily
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', video_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        
        try:
            # Analyze the video
            result = analyze_video(temp_path)
            if all(value is None for value in result.values()):
                logger.error(f"No valid predictions for video: {video_file.name}")
                return Response({"error": "Unable to analyze video. No valid predictions."}, 
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            # Format the result as a clean text
            formatted_result = self.format_result(result)
            return Response({"result": formatted_result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error analyzing video {video_file.name}: {str(e)}")
            return Response({"error": f"Error analyzing video: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def format_result(self, result):
        formatted_lines = [
            f"Batsman Position: {result['batsman_position'].capitalize()}",
            f"Shot Type: {result['shot_type'].capitalize()}",
            f"Stance Analysis: {result['stance_analysis'].capitalize()}",
            f"Footwork: {result['footwork'].capitalize()}"
        ]
        return "\n".join(formatted_lines)

