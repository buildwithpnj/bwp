import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.action_execution_service import ActionExecutionService
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_action_execution_flow():
    db = AsyncMock()
    
    async def mock_refresh(obj):
        obj.id = "log_123"
    db.refresh = mock_refresh
    
    # Mock scalars().all() for idempotency guard (no existing logs)
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = []
    db.execute.return_value = mock_res
    
    # Executing auto-approved safe action via new queued flow
    payload = {"original": "me goes", "corrected": "I go", "explanation": "Grammar fix"}
    with patch("app.services.idempotency_guard.IdempotencyGuard.validate_and_gate", AsyncMock(return_value=("key_123", True))):
        with patch("app.services.job_enqueuer.JobEnqueuer.enqueue_action", AsyncMock(return_value="job_123")):
            res = await ActionExecutionService.request_execution(
                db=db,
                user_id="user_123",
                user_role="approved_user",
                action_name="save_corrected_example",
                payload=payload
            )
    assert res["status"] == "queued"
    assert res["job_id"] == "job_123"
    db.commit.assert_called()

def test_agent_action_execution_flow():
    # Safe auto action
    res = ActionExecutionService.execute_action("create_note", {"content": "text"}, "tenant_1")
    assert res["status"] == "success"
    
    # Confirm first pending approval
    res_pending = ActionExecutionService.execute_action("delete_all_files", {}, "tenant_1")
    assert res_pending["status"] == "pending_approval"
    
    # Bypass gates to simulate success after approval
    from app.llm_settings import llm_settings
    with patch.object(llm_settings, "approval_gates_enabled", False):
        res_approved = ActionExecutionService.execute_action("delete_all_files", {}, "tenant_1")
        assert res_approved["status"] == "success"
    
    # Rollback simulation
    res_fail = ActionExecutionService.execute_action("fail_action", {}, "tenant_1")
    assert res_fail["status"] == "rolled_back"
