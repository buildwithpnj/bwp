import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.partial_failure_handler import PartialFailureHandler
from app.models.action_models import ActionLog
from app.models.notes import Note
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus

@pytest.mark.asyncio
async def test_partial_failure_rollback_note():
    db = AsyncMock()
    log = ActionLog(
        user_id="user_123",
        action_name="create_lesson_note",
        result_payload={"note_id": "note_999"},
        execution_status=ActionExecutionStatus.FAILED,
        recovery_status=ActionRecoveryStatus.NONE
    )
    
    with patch("app.services.action_rollback_service.ActionRollbackService._rollback_create_lesson_note", AsyncMock(return_value=True)) as mock_rb_note:
        await PartialFailureHandler.handle_partial_failure(db, log, Exception("Commit crashed"))
        
        assert log.execution_status == ActionExecutionStatus.ROLLED_BACK
        assert log.recovery_status == ActionRecoveryStatus.RECOVERED
        assert log.rolled_back_at is not None
        mock_rb_note.assert_called_once_with(db, log)
