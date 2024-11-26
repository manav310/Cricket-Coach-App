from django.urls import path
from .views import BallPlacementAnalysisView

urlpatterns = [
    path('analyze/ball-placement/', BallPlacementAnalysisView.as_view(), name='ball_placement_analysis'),
]
