from django.urls import path
from .views import TimingAnalysisView

urlpatterns = [
    path('analyze/timing/', TimingAnalysisView.as_view(), name='timing_analysis'),
]
