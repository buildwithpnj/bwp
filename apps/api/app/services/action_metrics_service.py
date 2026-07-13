from typing import Dict, Any, List, Optional
from collections import defaultdict
import time

class ActionMetricsService:
    # Local in-memory metrics store
    _metrics: Dict[str, int] = defaultdict(int)
    _execution_latencies: List[float] = []
    _approval_latencies: List[float] = []
    _action_failures: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    _user_counts: Dict[str, int] = defaultdict(int)
    _role_counts: Dict[str, int] = defaultdict(int)
    _duplicate_blocked_count: int = 0

    @classmethod
    def record_event(
        cls, 
        event_name: str, 
        user_id: str, 
        action_name: str, 
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """Records an event and updates aggregations in-memory."""
        cls._metrics[event_name] += 1
        cls._user_counts[user_id] += 1
        
        if event_name == "action_duplicate_blocked":
            cls._duplicate_blocked_count += 1
        
        if extra:
            if "user_role" in extra:
                cls._role_counts[extra["user_role"]] += 1
            if "latency_ms" in extra:
                latency = extra["latency_ms"] / 1000.0
                if event_name == "action_succeeded":
                    cls._execution_latencies.append(latency)
                elif event_name == "action_approved":
                    cls._approval_latencies.append(latency)
            if "error_type" in extra:
                cls._action_failures[action_name].append({
                    "timestamp": extra.get("timestamp"),
                    "error_type": extra.get("error_type"),
                    "error_message": extra.get("error_message")
                })

    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Returns a snapshot of system action health metrics."""
        avg_exec_latency = (
            sum(cls._execution_latencies) / len(cls._execution_latencies)
            if cls._execution_latencies else 0.0
        )
        avg_appr_latency = (
            sum(cls._approval_latencies) / len(cls._approval_latencies)
            if cls._approval_latencies else 0.0
        )
        
        # Calculate rates
        suggested = cls._metrics.get("action_suggested", 0)
        approved = cls._metrics.get("action_approved", 0)
        rejected = cls._metrics.get("action_rejected", 0)
        total_approvals = approved + rejected
        approval_rate = (approved / total_approvals) if total_approvals > 0 else 0.0
        
        queued = cls._metrics.get("action_queued", 0)
        succeeded = cls._metrics.get("action_succeeded", 0)
        failed = cls._metrics.get("action_failed", 0)
        total_runs = succeeded + failed
        success_rate = (succeeded / total_runs) if total_runs > 0 else 0.0
        
        return {
            "counters": dict(cls._metrics),
            "averages": {
                "average_execution_latency_seconds": avg_exec_latency,
                "average_approval_latency_seconds": avg_appr_latency
            },
            "rates": {
                "approval_accept_rate": approval_rate,
                "execution_success_rate": success_rate,
                "duplicate_blocked_rate": cls._duplicate_blocked_count
            },
            "failures": dict(cls._action_failures),
            "users": dict(cls._user_counts),
            "roles": dict(cls._role_counts)
        }

    @classmethod
    def reset_metrics(cls) -> None:
        """Resets all metrics. Useful for testing."""
        cls._metrics.clear()
        cls._execution_latencies.clear()
        cls._approval_latencies.clear()
        cls._action_failures.clear()
        cls._user_counts.clear()
        cls._role_counts.clear()
        cls._duplicate_blocked_count = 0
