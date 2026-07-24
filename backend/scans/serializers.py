from rest_framework import serializers

from projects.models import Project
from scans.models import ScanJob
from scans.tasks import process_scan_job


class ScanJobSerializer(serializers.ModelSerializer):
    scan_job_id = serializers.IntegerField(source="id", read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        source="project",
        queryset=Project.objects.none(),
        write_only=True,
    )
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ScanJob
        fields = (
            "id",
            "scan_job_id",
            "project",
            "project_id",
            "source_file",
            "status",
            "scan_type",
            "error_message",
            "metadata",
            "started_at",
            "finished_at",
            "created_date",
            "updated_date",
        )
        read_only_fields = (
            "id",
            "scan_job_id",
            "project",
            "status",
            "error_message",
            "metadata",
            "started_at",
            "finished_at",
            "created_date",
            "updated_date",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["project_id"].queryset = Project.objects.filter(
                owner=request.user,
                active=True,
            )

    def validate_source_file(self, source_file):
        if not source_file.name.lower().endswith(".zip"):
            raise serializers.ValidationError("source_file must be a .zip file.")
        return source_file

    def create(self, validated_data):
        request = self.context["request"]
        source_file = validated_data["source_file"]
        metadata = dict(validated_data.get("metadata") or {})
        metadata["source_file_name"] = source_file.name

        validated_data["metadata"] = metadata
        validated_data["created_by"] = request.user
        validated_data["status"] = ScanJob.Status.PENDING

        scan_job = super().create(validated_data)
        process_scan_job.delay(scan_job.id)

        return scan_job


class ScanJobStatusSerializer(serializers.ModelSerializer):
    scan_job_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = ScanJob
        fields = (
            "scan_job_id",
            "status",
            "error_message",
            "started_at",
            "finished_at",
            "updated_date",
        )
