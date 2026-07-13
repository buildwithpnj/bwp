from app.services.loop_orchestrator import LoopOrchestrator

def test_loop_orchestration():
    res = LoopOrchestrator.execute_loop("sync configuration B", "tenant_123")
    assert res["completed_steps"] > 0
    assert res["outcome"] == "success"
