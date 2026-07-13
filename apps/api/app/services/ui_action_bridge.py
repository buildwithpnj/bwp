import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.action_models import ActionLog

class UiActionBridge:
    @classmethod
    async def bridge_action_to_runner(
        cls,
        db: AsyncSession,
        action_name: str,
        payload: Dict[str, Any]
    ) -> str:
        """
        Translates Copilot intents and schedules them onto the standard ActionLog queue.
        """
        log_id = f"act_{uuid.uuid4().hex[:8]}"
        log = ActionLog(
            id=log_id,
            action_name=action_name,
            payload=payload,
            execution_status="pending",
            requires_approval=True
        )
        db.add(log)
        await db.commit()
        return log_id
