import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.action_execution_service import ActionExecutionService
from app.models.action_models import ActionLog

@pytest.mark.asyncio
async def test_action_execution_flow():
    db = AsyncMock()
    
    async def mock_refresh(obj):
        obj.id = "log_123"
    db.refresh = mock_refresh
    
    # Mock db.execute returning None to simulate progress check
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res
    
    # Executing auto-approved safe action
    payload = {"original": "me goes", "corrected": "I go", "explanation": "Grammar fix"}
    res = await ActionExecutionService.request_execution(
        db=db,
        user_id="user_123",
        user_role="approved_user",
        action_name="save_corrected_example",
        payload=payload
    )
    assert res["status"] == "success"
    db.commit.assert_called()
