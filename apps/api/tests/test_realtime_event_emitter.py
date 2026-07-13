import pytest
from unittest.mock import AsyncMock, patch
from app.services.realtime_event_emitter import RealTimeEventEmitter

@pytest.mark.asyncio
async def test_realtime_event_emitter_broadcast():
    with patch("app.realtime.websocket_manager.WebSocketManager.broadcast_event", AsyncMock()) as mock_broadcast:
        await RealTimeEventEmitter.emit_action_event(
            event_type="action.executing",
            action_log_id="log_123",
            action_name="create_lesson_note",
            user_id="user_123",
            execution_status="executing",
            summary_message="Doing work"
        )
        
        mock_broadcast.assert_called_once()
        event = mock_broadcast.call_args[0][0]
        assert event.event_type == "action.executing"
        assert event.action_log_id == "log_123"
        assert event.user_id == "user_123"
