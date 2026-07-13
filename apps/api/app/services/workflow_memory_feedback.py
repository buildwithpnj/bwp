import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.user_profile_memory_service import UserProfileMemoryService

logger = logging.getLogger("workflow_memory_feedback")

class WorkflowMemoryFeedback:
    @classmethod
    async def apply_memory_update(
        cls,
        db: AsyncSession,
        user_id: str,
        topic: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Feeds successful workflow results into memory updates while explaining changes.
        """
        logger.info(f"Applying workflow feedback memory updates for user {user_id}. Topic: {topic}")
        
        # Verify safety or sanitization (non-blind writes)
        sanitized_updates = {}
        for k, v in updates.items():
            if k in ["tone", "explanation_style", "preferred_language"]:
                sanitized_updates[k] = v
                
        if not sanitized_updates:
            logger.warning("No safe attributes found to write to user profile memory.")
            return False
            
        await UserProfileMemoryService.update_profile(db, user_id, sanitized_updates)
        logger.info(f"Successfully applied memory updates: {sanitized_updates}")
        return True
