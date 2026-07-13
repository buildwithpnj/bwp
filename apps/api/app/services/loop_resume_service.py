import logging
from typing import Dict, Any, Optional
from app.services.persistent_loop_state_store import PersistentLoopStateStore

logger = logging.getLogger("loop_resume")

class LoopResumeService:
    @classmethod
    def resume_loop(cls, state_id: str) -> Optional[Dict[str, Any]]:
        """
        Loads saved checkpoint details.
        """
        state = PersistentLoopStateStore.get_state(state_id)
        if not state:
            logger.error(f"No checkpoint trace found for state ID: {state_id}")
            return None

        logger.info(f"Successfully resumed run from checkpoint state: {state_id}")
        return state
