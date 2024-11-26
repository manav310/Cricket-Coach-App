from django.urls import path
from .views import BallSpeedAnalysisView

urlpatterns = [
    path('analyze/ball-speed/', BallSpeedAnalysisView.as_view(), name='ball-speed-analysis')
]

# Note: Updated the URL pattern to be consistent with other analysis endpoints
