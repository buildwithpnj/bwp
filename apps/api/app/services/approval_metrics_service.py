from typing import Dict

class ApprovalMetricsService:
    # Central metrics counters in-memory
    _metrics = {
        "created": 0,
        "approved": 0,
        "denied": 0,
        "expired": 0,
        "auto_executed": 0,
        "blocked": 0,
        "destructive_requested": 0,
        "destructive_executed": 0,
        "verifier_failures": 0,
        "leak_prevented": 0
    }

    @classmethod
    def increment_created_count(cls):
        cls._metrics["created"] += 1

    @classmethod
    def increment_approved_count(cls):
        cls._metrics["approved"] += 1

    @classmethod
    def increment_denied_count(cls):
        cls._metrics["denied"] += 1

    @classmethod
    def increment_expired_count(cls):
        cls._metrics["expired"] += 1

    @classmethod
    def increment_auto_executed_count(cls):
        cls._metrics["auto_executed"] += 1

    @classmethod
    def increment_blocked_count(cls):
        cls._metrics["blocked"] += 1

    @classmethod
    def increment_destructive_requested_count(cls):
        cls._metrics["destructive_requested"] += 1

    @classmethod
    def increment_destructive_executed_count(cls):
        cls._metrics["destructive_executed"] += 1

    @classmethod
    def increment_verifier_failure_count(cls):
        cls._metrics["verifier_failures"] += 1

    @classmethod
    def increment_leak_prevention_count(cls):
        cls._metrics["leak_prevented"] += 1

    @classmethod
    def get_metrics(cls) -> Dict[str, int]:
        return cls._metrics.copy()

    @classmethod
    def reset_metrics(cls):
        for k in cls._metrics:
            cls._metrics[k] = 0
