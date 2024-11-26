from django.db import models

class BallSpeedVideo(models.Model):
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ball Speed Video {self.id}"

# Note: Remove the 'speed' field as we'll calculate it on-the-fly like in the body stance analysis
