from django.shortcuts import render

# Create your views here.

# analysis/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_video(request):
    if 'file' not in request.FILES:
        logger.warning("No file provided in the request")
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    video = Video(file=request.FILES['file'])
    video.save()
    logger.info(f"Video saved with ID: {video.id}")
    serializer = VideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

""" @api_view(['POST'])
def record_video(request):
    # For now, this endpoint will be similar to upload_video
    # In the future, you might want to implement real-time video recording
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    video = Video(file=request.FILES['file'])
    video.save()
    serializer = VideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_201_CREATED) """

