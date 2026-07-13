import logging
from fastapi import WebSocket
from typing import Dict, List, Set, Optional, Any
from app.schemas.realtime_event import RealTimeEvent

logger = logging.getLogger("websocket_manager")

class WebSocketManager:
    # Active connection maps: user_id -> List[WebSocket]
    _user_connections: Dict[str, List[WebSocket]] = {}
    # Connection details: websocket -> metadata dict (role, tenant_id, etc.)
    _connection_meta: Dict[WebSocket, Dict[str, Any]] = {}
    
    @classmethod
    async def connect(
        cls,
        websocket: WebSocket,
        user_id: str,
        user_role: str,
        tenant_id: Optional[str] = None
    ) -> None:
        """Accepts a live WebSocket connection and logs it to connection mapping registry."""
        await websocket.accept()
        if user_id not in cls._user_connections:
            cls._user_connections[user_id] = []
        cls._user_connections[user_id].append(websocket)
        
        cls._connection_meta[websocket] = {
            "user_id": user_id,
            "role": user_role,
            "tenant_id": tenant_id
        }
        logger.info(f"WebSocket connected. user_id={user_id} role={user_role}")

    @classmethod
    def disconnect(cls, websocket: WebSocket) -> None:
        """Removes a WebSocket connection from registry."""
        meta = cls._connection_meta.pop(websocket, None)
        if meta:
            user_id = meta["user_id"]
            if user_id in cls._user_connections:
                cls._user_connections[user_id].remove(websocket)
                if not cls._user_connections[user_id]:
                    cls._user_connections.pop(user_id)
            logger.info(f"WebSocket disconnected for user_id={user_id}")

    @classmethod
    async def send_event_to_user(cls, user_id: str, event: RealTimeEvent) -> None:
        """Pushes an event directly to all socket connections of a specific user."""
        connections = cls._user_connections.get(user_id, [])
        for ws in list(connections):
            try:
                await ws.send_text(event.model_dump_json())
            except Exception as e:
                logger.error(f"Error sending event to user {user_id}: {e}")
                cls.disconnect(ws)

    @classmethod
    async def broadcast_event(cls, event: RealTimeEvent) -> None:
        """
        Broadcasts an event globally while respecting tenant isolation & role rules:
        - Admin users receive ALL events.
        - Regular users only receive events where event.user_id matches their user_id.
        """
        for ws, meta in list(cls._connection_meta.items()):
            role = meta["role"]
            user_id = meta["user_id"]
            
            # Authorization / Tenant Isolation check
            is_admin = (role == "internal_admin")
            is_owner = (user_id == event.user_id)
            
            if is_admin or is_owner:
                try:
                    await ws.send_text(event.model_dump_json())
                except Exception as e:
                    logger.error(f"Error broadcasting event to websocket: {e}")
                    cls.disconnect(ws)

    @classmethod
    def get_connection_count(cls) -> int:
        return len(cls._connection_meta)

    @classmethod
    def clear_connections(cls) -> None:
        cls._user_connections.clear()
        cls._connection_meta.clear()
