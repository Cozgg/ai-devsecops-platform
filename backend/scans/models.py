from django.conf import settings
from django.db import models

from common.models import TimeStampedModel
from projects.models import Project


class ScanJob(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    class ScanType(models.TextChoices):
        SAST = "SAST", "SAST"
        DEPENDENCY = "DEPENDENCY", "Dependency"
        FULL = "FULL", "Full"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="scan_jobs")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="scan_jobs",
    )
    source_file = models.FileField(upload_to="source_uploads/")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    scan_type = models.CharField(max_length=20, choices=ScanType.choices, default=ScanType.FULL)
    error_message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "scans_scan_job"
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["created_date"]),
        ]

    def __str__(self):
        return f"{self.project.name} - {self.status}"
