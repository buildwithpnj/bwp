import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.action_models import ActionLog
from app.models.notes import Note
from app.models.learning_progress import LearningProgress
from app.models.action_execution_state import ActionExecutionStatus, ActionRecoveryStatus
from app.services.action_observability_service import ActionObservabilityService

logger = logging.getLogger("action_rollback")

class ActionRollbackService:
    @classmethod
    async def rollback(cls, db: AsyncSession, log: ActionLog) -> bool:
        """
        Attempts compensating actions to rollback partial changes.
        Returns:
            bool: True if rollback succeeded, False if it failed.
        """
        logger.info(f"Initiating rollback for action={log.action_name} id={log.id}")
        ActionObservabilityService.log_event(
            event_name="action_rollback_started",
            user_id=log.user_id,
            action_name=log.action_name,
            action_log_id=log.id
        )
        
        try:
            success = False
            if log.action_name == "create_lesson_note":
                success = await cls._rollback_create_lesson_note(db, log)
            elif log.action_name == "save_corrected_example":
                success = await cls._rollback_save_corrected_example(db, log)
            elif log.action_name == "mark_pattern_mastered":
                success = await cls._rollback_mark_pattern_mastered(db, log)
            else:
                # No specific rollback compensation needed for other actions
                success = True
                
            if success:
                from datetime import datetime, timezone
                log.execution_status = ActionExecutionStatus.ROLLED_BACK
                log.recovery_status = ActionRecoveryStatus.RECOVERED
                log.rolled_back_at = log.completed_at or log.updated_at or datetime.now(timezone.utc)
                await db.commit()
                
                ActionObservabilityService.log_event(
                    event_name="action_rolled_back",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id
                )
                return True
            else:
                log.recovery_status = ActionRecoveryStatus.RECOVERY_FAILED
                await db.commit()
                
                ActionObservabilityService.log_event(
                    event_name="action_rollback_failed",
                    user_id=log.user_id,
                    action_name=log.action_name,
                    action_log_id=log.id,
                    extra={"error": "Rollback compensation returned False"}
                )
                return False
                
        except Exception as e:
            logger.exception(f"Exception during rollback for action={log.id}")
            log.recovery_status = ActionRecoveryStatus.RECOVERY_FAILED
            log.last_error = f"Rollback Exception: {str(e)}"
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="action_rollback_failed",
                user_id=log.user_id,
                action_name=log.action_name,
                action_log_id=log.id,
                extra={"error": str(e)}
            )
            return False

    @classmethod
    async def _rollback_create_lesson_note(cls, db: AsyncSession, log: ActionLog) -> bool:
        """Deletes the note created by this action log."""
        note_id = log.result_payload.get("note_id") if log.result_payload else None
        if not note_id:
            logger.warning(f"No note_id found in result payload for action log={log.id}, attempting fallback deletion by title")
            # Fallback: title/content search
            title = log.input_payload.get("title")
            if title:
                stmt = delete(Note).where(Note.user_id == log.user_id, Note.title == title)
                await db.execute(stmt)
                await db.commit()
                return True
            return False
            
        stmt = delete(Note).where(Note.id == note_id, Note.user_id == log.user_id)
        await db.execute(stmt)
        await db.commit()
        return True

    @classmethod
    async def _rollback_save_corrected_example(cls, db: AsyncSession, log: ActionLog) -> bool:
        """Reverses learning progress increment."""
        result = await db.execute(select(LearningProgress).where(LearningProgress.user_id == log.user_id))
        progress = result.scalar_one_or_none()
        if progress:
            if progress.corrections_accepted > 0:
                progress.corrections_accepted -= 1
            if progress.streak > 0:
                progress.streak -= 1
            # Remove from mastered patterns if sentence correction was saved as a pattern
            mastered = list(progress.mastered_patterns or [])
            if "sentence_correction" in mastered:
                mastered.remove("sentence_correction")
                progress.mastered_patterns = mastered
            await db.commit()
        return True

    @classmethod
    async def _rollback_mark_pattern_mastered(cls, db: AsyncSession, log: ActionLog) -> bool:
        """Removes the grammar pattern from mastered checklist."""
        pattern_name = log.input_payload.get("pattern_name")
        if not pattern_name:
            return False
            
        result = await db.execute(select(LearningProgress).where(LearningProgress.user_id == log.user_id))
        progress = result.scalar_one_or_none()
        if progress:
            mastered = list(progress.mastered_patterns or [])
            if pattern_name in mastered:
                mastered.remove(pattern_name)
                progress.mastered_patterns = mastered
            if progress.corrections_accepted > 0:
                progress.corrections_accepted -= 1
            if progress.streak > 0:
                progress.streak -= 1
            await db.commit()
        return True
