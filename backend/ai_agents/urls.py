from django.urls import path

from ai_agents.views import GenerateAIReportAPIView, ScanJobAIReportAPIView

urlpatterns = [
    path("scans/<int:scan_job_id>/generate/", GenerateAIReportAPIView.as_view(), name="generate-ai-report"),
    path("scans/<int:scan_job_id>/", ScanJobAIReportAPIView.as_view(), name="scan-job-ai-report"),
]
