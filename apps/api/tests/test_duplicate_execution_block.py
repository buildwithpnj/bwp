import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.action_execution_service import ActionExecutionService
from app.services.idempotency_guard import DuplicateRequestException

@pytest.mark.asyncio
async def test_duplicate_execution_block_in_orchestrator():
    db = AsyncMock()
    
    # Mock IdempotencyGuard.validate_and_gate to raise DuplicateRequestException
    with patch("app.services.idempotency_guard.IdempotencyGuard.validate_and_gate", AsyncMock(side_effect=DuplicateRequestException("Action is already in progress"))):
        res = await ActionExecutionService.request_execution(
            db=db,
            user_id="user_123",
            user_role="approved_user",
            action_name="save_corrected_example",
            payload={"original": "me goes", "corrected": "I go", "explanation": "Grammar fix"}
        )
        
        assert res["status"] == "failed"
        assert "Duplicate request" in res["error"]
        assert res.get("idempotency_blocked") is True
