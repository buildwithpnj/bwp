import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.schemas.realtime_event import RealTimeEvent
from app.realtime.websocket_manager import WebSocketManager

logger = logging.getLogger("realtime_event_emitter")

class RealTimeEventEmitter:
    @classmethod
    async def emit_action_event(
        cls,
        event_type: str,
        action_log_id: str,
        action_name: str,
        user_id: str,
        execution_status: str,
        summary_message: str,
        recovery_status: str = "none",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Constructs and broadcasts a WebSocket real-time action event.
        """
        event = RealTimeEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            occurred_at=datetime.now(timezone.utc),
            user_id=user_id,
            action_log_id=action_log_id,
            execution_status=execution_status,
            recovery_status=recovery_status,
            summary_message=summary_message,
            safe_metadata=metadata or {}
        )
        
        logger.info(f"Emitting realtime action event: {event_type} for log={action_log_id}")
        await WebSocketManager.broadcast_event(event)

    @classmethod
    async def emit_workflow_event(
        cls,
        event_type: str,
        workflow_run_id: str,
        user_id: str,
        status: str,
        summary_message: str,
        step_index: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Constructs and broadcasts a WebSocket real-time workflow event.
        """
        meta = metadata or {}
        if step_index is not None:
            meta["step_index"] = step_index
            
        event = RealTimeEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            occurred_at=datetime.now(timezone.utc),
            user_id=user_id,
            workflow_run_id=workflow_run_id,
            execution_status=status,
            summary_message=summary_message,
            safe_metadata=meta
        )
        
        logger.info(f"Emitting realtime workflow event: {event_type} for workflow={workflow_run_id}")
        await WebSocketManager.broadcast_event(event)
