import pytest
from app.services.loop_resume_service import LoopResumeService
from app.services.persistent_loop_state_store import PersistentLoopStateStore

def test_loop_resume_success():
    state_id = "test-resume-1"
    PersistentLoopStateStore.save_state(
        state_id=state_id,
        prompt="sync files",
        tenant_id="tenant_1",
        steps=[{"step": 1}],
        evidence=[],
        status="active"
    )
    
    resumed = LoopResumeService.resume_loop(state_id)
    assert resumed is not None
    assert resumed["state_id"] == state_id
    assert resumed["status"] == "active"
