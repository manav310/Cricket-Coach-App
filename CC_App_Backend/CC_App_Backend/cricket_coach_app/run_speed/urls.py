from django.urls import path
from .views import ProcessVideoView

urlpatterns = [
    path('analyze/runningspeed/', ProcessVideoView.as_view(), name='analyze_running_speed'),
]
