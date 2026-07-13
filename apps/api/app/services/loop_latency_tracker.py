import time
from typing import List

class LoopLatencyTracker:
    _step_latencies: List[float] = []

    @classmethod
    def record_step_latency(cls, duration: float) -> None:
        cls._step_latencies.append(duration)

    @classmethod
    def get_average_step_latency(cls) -> float:
        if not cls._step_latencies:
            return 0.0
        return sum(cls._step_latencies) / len(cls._step_latencies)

    @classmethod
    def clear_latencies(cls) -> None:
        cls._step_latencies.clear()
