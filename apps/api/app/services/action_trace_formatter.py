from typing import List
from app.models.action_models import ActionLog

class ActionTraceFormatter:
    @classmethod
    def format_trace(cls, log: ActionLog) -> str:
        """Formats the lifecycle log record as a human-readable diagnostic timeline."""
        lines: List[str] = []
        lines.append(f"=== Action Execution Trace: {log.action_name} ===")
        lines.append(f"Log ID: {log.id}")
        lines.append(f"User ID: {log.user_id}")
        lines.append(f"Idempotency Key: {log.idempotency_key or 'None'}")
        lines.append(f"Status: {log.execution_status.upper()} (Recovery: {log.recovery_status.upper()})")
        lines.append("Timeline:")

        timestamps = [
            ("Suggested At", log.suggested_at),
            ("Approved At", log.approved_at),
            ("Queued At", log.queued_at),
            ("Execution Started At", log.execution_started_at),
            ("Executed/Succeeded At", log.executed_at),
            ("Failed At", log.failed_at),
            ("Rolled Back At", log.rolled_back_at),
        ]

        # Filter out unset timestamps and sort
        active_timeline = [(name, ts) for name, ts in timestamps if ts is not None]
        active_timeline.sort(key=lambda x: x[1])

        if not active_timeline:
            lines.append("  (No lifecycle timestamps recorded)")
            return "\n".join(lines)

        base_time = active_timeline[0][1]
        for name, ts in active_timeline:
            delta = (ts - base_time).total_seconds()
            lines.append(f"  +{delta:6.3f}s | {name} ({ts.isoformat()})")

        if log.last_error:
            lines.append(f"Last Error Diagnosed: {log.last_error}")
            
        if log.retry_count > 0:
            lines.append(f"Retries Attempted: {log.retry_count} / {log.max_retries}")

        return "\n".join(lines)
