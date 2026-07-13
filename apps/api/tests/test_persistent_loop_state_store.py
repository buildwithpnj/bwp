import pytest
from app.services.persistent_loop_state_store import PersistentLoopStateStore

def test_persistent_loop_state_store_save_get():
    state_id = "test-uuid-1"
    PersistentLoopStateStore.save_state(
        state_id=state_id,
        prompt="sync files",
        tenant_id="tenant_1",
        steps=[{"step_index": 1}],
        evidence=[{"chunk_id": "c1"}],
        status="completed"
    )
    
    state = PersistentLoopStateStore.get_state(state_id)
    assert state is not None
    assert state["prompt"] == "sync files"
    assert state["status"] == "completed"
    assert len(state["steps"]) == 1
