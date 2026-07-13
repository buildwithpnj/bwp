import time
from typing import Dict, Any, List

class LocalLlmMetricsService:
    # Memory buffers to hold historical metrics
    _latency_history: List[float] = []
    _token_speed_history: List[float] = []
    _total_completions: int = 0
    _json_failures: int = 0
    _json_repairs: int = 0
    _fallback_triggers: int = 0
    _grounding_passes: int = 0
    _grounding_fails: int = 0

    @classmethod
    def record_completion(
        cls,
        latency: float,
        prompt_tokens: int,
        completion_tokens: int,
        status: str,
        json_mode: bool = False,
        json_repaired: bool = False,
        fallback_triggered: bool = False,
        grounding_passed: bool = True
    ):
        """
        Logs completion run statistics into memory cache counters.
        """
        cls._total_completions += 1
        cls._latency_history.append(latency)
        
        if completion_tokens > 0 and latency > 0:
            tokens_per_sec = completion_tokens / latency
            cls._token_speed_history.append(tokens_per_sec)

        if fallback_triggered:
            cls._fallback_triggers += 1

        if json_mode:
            if status == "error":
                cls._json_failures += 1
            if json_repaired:
                cls._json_repairs += 1

        if grounding_passed:
            cls._grounding_passes += 1
        else:
            cls._grounding_fails += 1

    @classmethod
    def get_summary_metrics(cls) -> Dict[str, Any]:
        """
        Calculates metric summary stats (p50, p95 latency, average speeds).
        """
        latencies = sorted(cls._latency_history)
        n = len(latencies)
        
        p50 = 0.0
        p95 = 0.0
        if n > 0:
            p50 = latencies[int(n * 0.5)]
            p95 = latencies[int(n * 0.95)] if n >= 20 else latencies[-1]

        avg_speed = 0.0
        if cls._token_speed_history:
            avg_speed = sum(cls._token_speed_history) / len(cls._token_speed_history)

        grounding_pass_rate = 1.0
        total_grounding = cls._grounding_passes + cls._grounding_fails
        if total_grounding > 0:
            grounding_pass_rate = cls._grounding_passes / total_grounding

        return {
            "total_completions": cls._total_completions,
            "avg_latency": sum(latencies) / n if n > 0 else 0.0,
            "p50_latency": p50,
            "p95_latency": p95,
            "avg_tokens_per_sec": avg_speed,
            "json_failure_count": cls._json_failures,
            "json_repair_count": cls._json_repairs,
            "fallback_trigger_count": cls._fallback_triggers,
            "grounding_pass_rate": grounding_pass_rate,
            "passes_count": cls._grounding_passes,
            "fails_count": cls._grounding_fails
        }
        
    @classmethod
    def clear_metrics(cls):
        cls._latency_history.clear()
        cls._token_speed_history.clear()
        cls._total_completions = 0
        cls._json_failures = 0
        cls._json_repairs = 0
        cls._fallback_triggers = 0
        cls._grounding_passes = 0
        cls._grounding_fails = 0
