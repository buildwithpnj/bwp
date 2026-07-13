from typing import Dict, Any

class RunTraceService:
    _traces = {}

    @classmethod
    def save_trace(cls, state_id: str, health_metrics: Dict[str, Any]) -> None:
        cls._traces[state_id] = {
            "state_id": state_id,
            "metrics": health_metrics
        }
