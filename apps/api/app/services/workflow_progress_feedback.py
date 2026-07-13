import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.learning_progress_service import LearningProgressService

logger = logging.getLogger("workflow_progress_feedback")

class WorkflowProgressFeedback:
    @classmethod
    async def apply_progress_update(
        cls,
        db: AsyncSession,
        user_id: str,
        actions_completed: int
    ) -> bool:
        """
        Increments user mastery streaks and progress counts based on workflow completion.
        """
        logger.info(f"Applying workflow progress feedback updates for user {user_id}.")
        
        # Drive learning progress record safely
        progress = await LearningProgressService.increment_correction_count(db, user_id, count=actions_completed)
        logger.info(f"Progress updated. New count: {progress.correction_count}")
        return True
