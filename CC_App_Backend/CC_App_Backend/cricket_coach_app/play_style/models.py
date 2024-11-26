from django.db import models

class Video(models.Model):
    analysis_name = models.CharField(max_length=100, default='Play Style')
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.analysis_name} - {self.analyzed_at}"

