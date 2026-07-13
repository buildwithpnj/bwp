import pytest
from app.services.loop_orchestrator import LoopOrchestrator

def test_execute_loop_steps_budget():
    result = LoopOrchestrator.execute_loop("sync my habits settings", "tenant_1")
    assert result["state_id"] is not None
    assert result["completed_steps"] > 0
    assert result["outcome"] in ("success", "insufficient_data")
