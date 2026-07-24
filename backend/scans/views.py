from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from scans.models import ScanJob
from scans.serializers import ScanJobSerializer, ScanJobStatusSerializer


class ScanJobViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "head", "options")
    serializer_class = ScanJobSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ScanJob.objects.filter(
            project__owner=self.request.user,
            project__active=True,
        ).select_related("project", "created_by").order_by("-created_date")

    @action(detail=True, methods=("get",), url_path="status")
    def get_scan_job_status(self, request, pk=None):
        scan_job = self.get_object()
        serializer = ScanJobStatusSerializer(scan_job)
        return Response(serializer.data)
