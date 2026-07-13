from typing import Dict, Any, Optional
from app.services.action_dispatcher import ActionDispatcher

class JobEnqueuer:
    @classmethod
    async def enqueue_action(
        cls,
        action_log_id: str,
        action_name: str,
        user_id: str,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        delay_seconds: int = 0
    ) -> str:
        """Helper to queue an individual action for worker pick up."""
        meta = metadata or {}
        if "queue_name" not in meta:
            meta["queue_name"] = "actions"
            
        return await ActionDispatcher.dispatch(
            action_log_id=action_log_id,
            action_name=action_name,
            user_id=user_id,
            idempotency_key=idempotency_key,
            metadata=meta,
            delay_seconds=delay_seconds
        )

    @classmethod
    async def enqueue_workflow_step(
        cls,
        workflow_run_id: str,
        step_index: int,
        user_id: str,
        delay_seconds: int = 0
    ) -> str:
        """Helper to queue a workflow run step."""
        meta = {
            "queue_name": "workflows",
            "workflow_run_id": workflow_run_id,
            "step_index": step_index
        }
        return await ActionDispatcher.dispatch(
            action_log_id="none",
            action_name="workflow_step",
            user_id=user_id,
            metadata=meta,
            delay_seconds=delay_seconds
        )
