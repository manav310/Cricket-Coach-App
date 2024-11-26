# analysis/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('analysis/upload/', views.upload_video, name='upload_video'),
    # path('analysis/record/', views.record_video, name='record_video'),
]

