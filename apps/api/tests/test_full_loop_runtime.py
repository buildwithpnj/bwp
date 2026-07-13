from app.services.full_loop_runtime import FullLoopRuntime

def test_full_loop_runtime():
    res = FullLoopRuntime.execute_full_run("sync Dev B parameters", "tenant_1")
    assert "state_id" in res
    assert "health_metrics" in res
