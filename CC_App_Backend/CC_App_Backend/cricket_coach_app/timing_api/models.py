from django.db import models

# Create your models here.

class UploadedVideo(models.Model):
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video uploaded at {self.uploaded_at}"
