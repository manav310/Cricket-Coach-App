from rest_framework import serializers
from .models import UploadedVideo

class UploadedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedVideo
        fields = ['id', 'video', 'uploaded_at']
