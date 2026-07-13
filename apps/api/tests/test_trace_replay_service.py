import pytest
from app.services.trace_replay_service import TraceReplayService
from app.services.persistent_loop_state_store import PersistentLoopStateStore

def test_trace_replay_success():
    state_id = "test-replay-1"
    PersistentLoopStateStore.save_state(
        state_id=state_id,
        prompt="sync files",
        tenant_id="tenant_1",
        steps=[{"step_index": 1}],
        evidence=[],
        status="completed",
        stop_reason="finished_plan"
    )
    
    replay = TraceReplayService.replay_trace(state_id)
    assert replay is not None
    assert replay["state_id"] == state_id
    assert replay["steps_taken"] == 1
    assert replay["stop_reason"] == "finished_plan"
