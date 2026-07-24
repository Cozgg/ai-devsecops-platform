from django.utils import timezone

from scans.models import ScanJob


class InvalidScanJobStateTransition(Exception):
    """xuat hien khi yeu cau transition sai trang thai."""


class ScanJobState:
    status = None

    def start(self, context):
        self._invalid_transition("start")

    def complete(self, context, metadata):
        self._invalid_transition("complete")

    def fail(self, context, error_message):
        self._invalid_transition("fail")

    def _invalid_transition(self, event):
        raise InvalidScanJobStateTransition(
            f"Cannot {event} scan job from {self.status} state."
        )


class PendingState(ScanJobState):
    status = ScanJob.Status.PENDING

    def start(self, context):
        context._transition_to(
            RunningState(),
            started_at=timezone.now(),
            error_message=None,
            update_fields=["status", "started_at", "error_message", "updated_date"],
        )


class RunningState(ScanJobState):
    status = ScanJob.Status.RUNNING

    def complete(self, context, metadata):
        context._transition_to(
            CompletedState(),
            metadata=metadata,
            finished_at=timezone.now(),
            update_fields=["metadata", "status", "finished_at", "updated_date"],
        )

    def fail(self, context, error_message):
        context._transition_to(
            FailedState(),
            error_message=error_message,
            finished_at=timezone.now(),
            update_fields=["status", "error_message", "finished_at", "updated_date"],
        )


class CompletedState(ScanJobState):
    status = ScanJob.Status.COMPLETED


class FailedState(ScanJobState):
    status = ScanJob.Status.FAILED


class ScanJobStateMachine:

    _states = {
        ScanJob.Status.PENDING: PendingState,
        ScanJob.Status.RUNNING: RunningState,
        ScanJob.Status.COMPLETED: CompletedState,
        ScanJob.Status.FAILED: FailedState,
    }

    def __init__(self, scan_job):
        try:
            state_class = self._states[scan_job.status]
        except KeyError as exc:
            raise InvalidScanJobStateTransition(
                f"Unknown scan job state: {scan_job.status}"
            ) from exc

        self.scan_job = scan_job
        self._state = state_class()

    @property
    def status(self):
        return self._state.status

    def start(self):
        self._state.start(self)

    def complete(self, metadata):
        self._state.complete(self, metadata)

    def fail(self, error_message):
        self._state.fail(self, error_message)

    def _transition_to(self, state, update_fields, **values):
        for field_name, value in values.items():
            setattr(self.scan_job, field_name, value)

        self.scan_job.status = state.status
        self.scan_job.save(update_fields=update_fields)
        self._state = state
