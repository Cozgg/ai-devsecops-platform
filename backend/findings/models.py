from django.db import models

from common.models import TimeStampedModel
from scans.models import ScanJob


class ScanFinding(TimeStampedModel):
    class Severity(models.TextChoices):
        INFO = "INFO", "Info"
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        FIXED = "FIXED", "Fixed"
        IGNORED = "IGNORED", "Ignored"

    scan_job = models.ForeignKey(ScanJob, on_delete=models.CASCADE, related_name="findings")
    scanner_name = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.INFO)
    description = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    line_number = models.IntegerField(blank=True, null=True)
    code_snippet = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "findings_scan_finding"
        indexes = [
            models.Index(fields=["scan_job", "severity"]),
            models.Index(fields=["status"]),
            models.Index(fields=["scanner_name"]),
        ]

    def __str__(self):
        return f"{self.severity} - {self.title}"
