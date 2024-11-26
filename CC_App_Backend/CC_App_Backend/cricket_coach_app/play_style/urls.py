from django.urls import path
from .views import AnalyzePlayStyleView

urlpatterns = [
    path('analyze/playstyle/', AnalyzePlayStyleView.as_view(), name='analyze_play_style'),
]

