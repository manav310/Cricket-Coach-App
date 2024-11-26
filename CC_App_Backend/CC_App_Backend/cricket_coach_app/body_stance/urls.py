from django.urls import path
from .views import VideoAnalysisView, DownloadPDFView, PreviousAnalysesView

urlpatterns = [
    path('analyze/bodystance/', VideoAnalysisView.as_view(), name='video_analysis'),
    path('download/pdf-bodystance/<str:pdf_id>/', DownloadPDFView.as_view(), name='download_pdf'),
    path('previous/bodystance/', PreviousAnalysesView.as_view(), name='previous_analyses'),
]

