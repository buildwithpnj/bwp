import logging
from typing import Dict, Any, List, Optional
from app.services.persistent_loop_state_store import PersistentLoopStateStore

logger = logging.getLogger("trace_replay")

class TraceReplayService:
    @classmethod
    def replay_trace(cls, state_id: str) -> Optional[Dict[str, Any]]:
        """
        Loads the history of steps, collected context, and final answer to inspect run integrity.
        """
        state = PersistentLoopStateStore.get_state(state_id)
        if not state:
            logger.error(f"Cannot find execution logs for trace ID: {state_id}")
            return None

        logger.info(f"Replaying trace log: {state_id}")
        return {
            "state_id": state_id,
            "prompt": state.get("prompt"),
            "tenant_id": state.get("tenant_id"),
            "steps_taken": len(state.get("steps") or []),
            "steps": state.get("steps"),
            "evidence": state.get("evidence"),
            "status": state.get("status"),
            "stop_reason": state.get("stop_reason")
        }
