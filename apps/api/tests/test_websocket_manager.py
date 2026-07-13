import pytest
from unittest.mock import AsyncMock, MagicMock
from app.realtime.websocket_manager import WebSocketManager
from app.schemas.realtime_event import RealTimeEvent
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_websocket_manager_connect_disconnect():
    WebSocketManager.clear_connections()
    
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    
    # Connect
    await WebSocketManager.connect(ws1, "user_1", "approved_user")
    await WebSocketManager.connect(ws2, "user_2", "internal_admin")
    
    assert WebSocketManager.get_connection_count() == 2
    
    # Broadcast event for user_1
    event = RealTimeEvent(
        event_id="evt_1",
        event_type="action.succeeded",
        occurred_at=datetime.now(timezone.utc),
        user_id="user_1",
        summary_message="Succeeded"
    )
    
    await WebSocketManager.broadcast_event(event)
    
    # ws1 (owner) and ws2 (admin) should receive it
    ws1.send_text.assert_called_once()
    ws2.send_text.assert_called_once()
    
    # Disconnect ws1
    WebSocketManager.disconnect(ws1)
    assert WebSocketManager.get_connection_count() == 1
