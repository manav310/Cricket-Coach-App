from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .utils import process_video
import tempfile
import os
import json

class ProcessVideoView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided"}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            result = process_video(temp_file_path)
            # Format the result as a clear text
            formatted_result = self.format_result(result)
            return Response({"result": formatted_result}, content_type='application/json')
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            os.unlink(temp_file_path)

    def format_result(self, result):
        formatted_lines = []
        for batsman_data in result:
            line = f"Batsman {batsman_data['batsman']}: Average Speed: {batsman_data['average_speed']} {batsman_data['unit']}"
            formatted_lines.append(line)
        return "\n".join(formatted_lines)

