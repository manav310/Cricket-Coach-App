from django.db import models

# Create your models here.

class Analysis(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='docs/')

    def __str__(self):
        return self.title

