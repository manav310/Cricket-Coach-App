from django import forms
from .models import UploadedVideo

class VideoForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ['video']

