from django.db import models

from common.models import TimeStampedModel
from scans.models import ScanJob


class AIReport(TimeStampedModel):
    scan_job = models.OneToOneField(
        ScanJob,
        on_delete=models.CASCADE,
        related_name="ai_report",
    )
    summary = models.TextField()
    risk_overview = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    report_json = models.JSONField(default=dict, blank=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "ai_agents_ai_report"
        indexes = [
            models.Index(fields=["created_date"]),
        ]

    def __str__(self):
        return f"AI Report for {self.scan_job_id}"
