import logging
from typing import List, Dict, Any
from app.services.persistent_loop_state_store import PersistentLoopStateStore

logger = logging.getLogger("loop_checkpoint")

class LoopCheckpointService:
    @classmethod
    def save_checkpoint(
        cls,
        state_id: str,
        prompt: str,
        tenant_id: str,
        steps: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]],
        status: str = "active"
    ) -> None:
        """
        Saves step execution details.
        """
        logger.info(f"Saving execution checkpoint for run: {state_id} (steps_count: {len(steps)})")
        PersistentLoopStateStore.save_state(
            state_id=state_id,
            prompt=prompt,
            tenant_id=tenant_id,
            steps=steps,
            evidence=evidence,
            status=status
        )
