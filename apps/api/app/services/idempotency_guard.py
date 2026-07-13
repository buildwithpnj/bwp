import hashlib
import json
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus

class IdempotencyException(Exception):
    pass

class DuplicateRequestException(IdempotencyException):
    """Raised when an identical execution request is already running or succeeded."""
    pass

class IllegalReExecutionException(IdempotencyException):
    """Raised when trying to re-execute a succeeded action log."""
    pass

class IdempotencyGuard:
    @classmethod
    def generate_key(cls, user_id: str, action_name: str, payload: Dict[str, Any]) -> str:
        """Generates a deterministic SHA-256 idempotency key from user, action, and inputs."""
        # Sort keys to ensure deterministic serialization of payloads
        serialized_payload = json.dumps(payload, sort_keys=True)
        raw_string = f"{user_id}:{action_name}:{serialized_payload}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()

    @classmethod
    async def validate_and_gate(
        cls, 
        db: AsyncSession, 
        user_id: str, 
        action_name: str, 
        payload: Dict[str, Any]
    ) -> Tuple[str, bool]:
        """
        Validates the request against execution records.
        Returns:
            Tuple[str, bool]: (idempotency_key, is_new_or_safe_retry)
        Raises:
            DuplicateRequestException: If currently executing or already succeeded.
        """
        key = cls.generate_key(user_id, action_name, payload)
        
        # Check database for existing logs matching the key
        stmt = select(ActionLog).where(
            ActionLog.idempotency_key == key
        ).order_by(ActionLog.created_at.desc())
        
        res = await db.execute(stmt)
        existing_logs = res.scalars().all()
        
        if not existing_logs:
            return key, True
            
        # Inspect latest execution state
        latest_log = existing_logs[0]
        
        if latest_log.execution_status in [ActionExecutionStatus.SUCCEEDED]:
            raise DuplicateRequestException("Action has already successfully completed.")
            
        if latest_log.execution_status in [ActionExecutionStatus.EXECUTING, ActionExecutionStatus.QUEUED]:
            raise DuplicateRequestException("Action is already in progress or queued for execution.")
            
        # If it failed or was rolled back, it might be retried if the policy allows
        return key, False
