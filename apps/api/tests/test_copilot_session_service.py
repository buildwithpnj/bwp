import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.copilot_session_service import CopilotSessionService
from app.models.copilot_session import CopilotSession

@pytest.mark.asyncio
async def test_copilot_session_lifecycle():
    db = AsyncMock()
    
    # Mock lookup
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res
    
    # 1. Create session
    sess = await CopilotSessionService.get_or_create_session(db, "usr_123")
    assert sess.user_id == "usr_123"
    assert sess.is_active is True
    
    # 2. Append message
    updated_sess = await CopilotSessionService.append_message(
        db, sess, "user", "Hello Warborn"
    )
    assert len(updated_sess.chat_history) == 1
    assert updated_sess.chat_history[0]["content"] == "Hello Warborn"
