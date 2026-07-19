from rest_framework import serializers

from ai_agents.models import AIReport


class AIReportSerializer(serializers.ModelSerializer):
    scan_job_id = serializers.IntegerField(source="scan_job.id", read_only=True)
    project_name = serializers.CharField(source="scan_job.project.name", read_only=True)

    class Meta:
        model = AIReport
        fields = (
            "id",
            "scan_job_id",
            "project_name",
            "summary",
            "risk_overview",
            "recommendation",
            "report_json",
            "model_name",
            "created_date",
            "updated_date",
        )
        read_only_fields = fields
