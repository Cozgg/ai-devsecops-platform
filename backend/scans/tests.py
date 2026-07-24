from unittest.mock import Mock

from django.test import TestCase

from scans.models import ScanJob
from scans.services.scan_job_state import (
    InvalidScanJobStateTransition,
    ScanJobStateMachine,
)


class ScanJobStateMachineTests(TestCase):
    def test_scan_job_can_move_from_pending_to_running(self):
        scan_job = Mock(status=ScanJob.Status.PENDING)
        state_machine = ScanJobStateMachine(scan_job)

        state_machine.start()

        self.assertEqual(state_machine.status, ScanJob.Status.RUNNING)
        self.assertEqual(scan_job.status, ScanJob.Status.RUNNING)
        scan_job.save.assert_called_once()

    def test_running_scan_job_can_complete_with_metadata(self):
        scan_job = Mock(status=ScanJob.Status.RUNNING)
        state_machine = ScanJobStateMachine(scan_job)
        metadata = {"source_extraction": {"extracted_files_count": 3}}

        state_machine.complete(metadata)

        self.assertEqual(state_machine.status, ScanJob.Status.COMPLETED)
        self.assertEqual(scan_job.metadata, metadata)
        scan_job.save.assert_called_once()

    def test_running_scan_job_can_fail(self):
        scan_job = Mock(status=ScanJob.Status.RUNNING)
        state_machine = ScanJobStateMachine(scan_job)

        state_machine.fail("Invalid ZIP archive")

        self.assertEqual(state_machine.status, ScanJob.Status.FAILED)
        self.assertEqual(scan_job.error_message, "Invalid ZIP archive")
        scan_job.save.assert_called_once()

    def test_completed_scan_job_cannot_be_started_again(self):
        scan_job = Mock(status=ScanJob.Status.COMPLETED)
        state_machine = ScanJobStateMachine(scan_job)

        with self.assertRaises(InvalidScanJobStateTransition):
            state_machine.start()
