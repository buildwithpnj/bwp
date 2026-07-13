import pytest
from app.services.action_observability_service import ActionObservabilityService
from app.services.action_metrics_service import ActionMetricsService

def test_action_observability_and_metrics():
    ActionMetricsService.reset_metrics()
    
    # Log some events
    ActionObservabilityService.log_event("action_suggested", "user_123", "create_lesson_note", "log_abc")
    ActionObservabilityService.log_event("action_succeeded", "user_123", "create_lesson_note", "log_abc", {"latency_ms": 150.0})
    ActionObservabilityService.log_event("action_duplicate_blocked", "user_123", "create_lesson_note", "none")
    
    summary = ActionMetricsService.get_summary()
    
    # Check counters
    assert summary["counters"]["action_suggested"] == 1
    assert summary["counters"]["action_succeeded"] == 1
    assert summary["counters"]["action_duplicate_blocked"] == 1
    
    # Check averages & rates
    assert summary["averages"]["average_execution_latency_seconds"] == 0.150
    assert summary["rates"]["duplicate_blocked_rate"] == 1
