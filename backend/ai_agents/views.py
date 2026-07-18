from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_agents.models import AIReport
from ai_agents.serializers import AIReportSerializer
from ai_agents.services.ai_report_service import generate_ai_report
from scans.models import ScanJob


def get_accessible_scan_job(user, scan_job_id):
    queryset = ScanJob.objects.select_related("project", "created_by")

    if not (user.is_staff or user.is_superuser):
        queryset = queryset.filter(project__owner=user, project__active=True)

    return get_object_or_404(queryset, pk=scan_job_id)


class GenerateAIReportAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, scan_job_id):
        scan_job = get_accessible_scan_job(request.user, scan_job_id)
        ai_report = generate_ai_report(scan_job)
        serializer = AIReportSerializer(ai_report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ScanJobAIReportAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, scan_job_id):
        scan_job = get_accessible_scan_job(request.user, scan_job_id)
        ai_report = get_object_or_404(AIReport, scan_job=scan_job)
        serializer = AIReportSerializer(ai_report)
        return Response(serializer.data)
