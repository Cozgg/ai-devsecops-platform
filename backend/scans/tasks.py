
from celery import shared_task

from scans.models import ScanJob
from scans.services.scan_job_state import ScanJobStateMachine
from scans.services.source_extractor import extract_source_archive_for_scan


@shared_task
def run_scan_job(scan_job_id):
    scan_job = ScanJob.objects.get(id=scan_job_id)
    state_machine = ScanJobStateMachine(scan_job)
    state_machine.start()

    try:
        extraction_result = extract_source_archive_for_scan(scan_job)

        metadata = dict(scan_job.metadata or {})
        metadata["worker"] = {
            "processed": True,
            "mode": "source_extraction",
            "message": "Celery worker extracted source code successfully.",
        }
        metadata["source_extraction"] = extraction_result

        state_machine.complete(metadata)

    except Exception as exc:
        state_machine.fail(str(exc))
        raise
