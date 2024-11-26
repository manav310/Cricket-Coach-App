from rest_framework import serializers
from .models import BallSpeedVideo

class BallSpeedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallSpeedVideo
        fields = ['id', 'video', 'uploaded_at']

# Note: We've removed the 'speed' field from the serializer
