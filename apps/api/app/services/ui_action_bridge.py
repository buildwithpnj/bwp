import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.action_models import ActionLog
from app.services.action_execution_service import ActionExecutionService

logger = logging.getLogger("ui_action_bridge")

class UiActionBridge:
    @classmethod
    async def bridge_action_to_runner(
        cls,
        db: AsyncSession,
        action_name: str,
        payload: Dict[str, Any],
        user_id: str
    ) -> str:
        """
        Translates Copilot intents and executes them synchronously for instant UI visual persistence.
        """
        log_id = f"act_{uuid.uuid4().hex[:8]}"
        log = ActionLog(
            id=log_id,
            user_id=user_id,
            action_name=action_name,
            input_payload=payload,
            status="pending",
            approval_status="auto_approved"
        )
        db.add(log)
        await db.flush()

        try:
            logger.info(f"Synchronously executing action '{action_name}' for user {user_id}...")
            await ActionExecutionService.execute_log_action(db, log)
        except Exception as e:
            logger.error(f"Failed synchronous execution of action '{action_name}': {e}")
            log.status = "failed"
            log.error_message = str(e)
            
        await db.commit()
        return log_id
