import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.idempotency_guard import IdempotencyGuard, DuplicateRequestException
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus

@pytest.mark.asyncio
async def test_generate_key():
    payload1 = {"title": "hello", "content": "world"}
    payload2 = {"content": "world", "title": "hello"}
    
    key1 = IdempotencyGuard.generate_key("user_123", "create_lesson_note", payload1)
    key2 = IdempotencyGuard.generate_key("user_123", "create_lesson_note", payload2)
    
    assert key1 == key2
    assert len(key1) == 64

@pytest.mark.asyncio
async def test_validate_and_gate_new():
    db = AsyncMock()
    # Mock db.execute returning empty list of logs
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = []
    db.execute.return_value = mock_res
    
    key, is_new = await IdempotencyGuard.validate_and_gate(
        db, "user_123", "create_lesson_note", {"title": "hello"}
    )
    assert is_new is True
    assert len(key) == 64

@pytest.mark.asyncio
async def test_validate_and_gate_duplicate_succeeded():
    db = AsyncMock()
    
    # Mock db.execute returning a succeeded log
    log = ActionLog(
        user_id="user_123",
        action_name="create_lesson_note",
        execution_status=ActionExecutionStatus.SUCCEEDED
    )
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = [log]
    db.execute.return_value = mock_res
    
    with pytest.raises(DuplicateRequestException, match="already successfully completed"):
        await IdempotencyGuard.validate_and_gate(
            db, "user_123", "create_lesson_note", {"title": "hello"}
        )

@pytest.mark.asyncio
async def test_validate_and_gate_duplicate_running():
    db = AsyncMock()
    
    # Mock db.execute returning an executing log
    log = ActionLog(
        user_id="user_123",
        action_name="create_lesson_note",
        execution_status=ActionExecutionStatus.EXECUTING
    )
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = [log]
    db.execute.return_value = mock_res
    
    with pytest.raises(DuplicateRequestException, match="already in progress or queued"):
        await IdempotencyGuard.validate_and_gate(
            db, "user_123", "create_lesson_note", {"title": "hello"}
        )
