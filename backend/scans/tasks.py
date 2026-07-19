
import time

from celery import shared_task
from django.utils import timezone

from scans.models import ScanJob


@shared_task
def run_scan_job(scan_job_id):
    scan_job = ScanJob.objects.get(id=scan_job_id)

    try:
        scan_job.status = ScanJob.Status.RUNNING
        scan_job.started_at = timezone.now()
        scan_job.error_message = None
        scan_job.save(update_fields=["status", "started_at", "error_message", "updated_date"])

        time.sleep(5)

        metadata = dict(scan_job.metadata or {})
        metadata["worker"] = {
            "processed": True,
            "mode": "simulation",
            "message": "Celery worker processed this scan job successfully.",
        }

        scan_job.metadata = metadata
        scan_job.status = ScanJob.Status.COMPLETED
        scan_job.finished_at = timezone.now()
        scan_job.save(update_fields=["metadata", "status", "finished_at", "updated_date"])

    except Exception as exc:
        scan_job.status = ScanJob.Status.FAILED
        scan_job.error_message = str(exc)
        scan_job.finished_at = timezone.now()
        scan_job.save(update_fields=["status", "error_message", "finished_at", "updated_date"])
        raise