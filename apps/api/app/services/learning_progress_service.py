from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.learning_progress import LearningProgress
from typing import Dict, Any, List

class LearningProgressService:
    @classmethod
    async def get_or_create_progress(cls, db: AsyncSession, user_id: str) -> LearningProgress:
        result = await db.execute(select(LearningProgress).where(LearningProgress.user_id == user_id))
        progress = result.scalar_one_or_none()
        if not progress:
            progress = LearningProgress(
                user_id=user_id,
                corrections_accepted=0,
                streak=0,
                mastered_patterns=[],
                weak_categories=[],
                prompt_categories_used=[],
                return_frequency=1
            )
            db.add(progress)
            await db.commit()
            await db.refresh(progress)
        return progress

    @classmethod
    async def record_correction(cls, db: AsyncSession, user_id: str, category: str, was_correct: bool = True):
        progress = await cls.get_or_create_progress(db, user_id)
        
        if was_correct:
            progress.corrections_accepted += 1
            progress.streak += 1
            # Add to mastered patterns list if not already there
            mastered = list(progress.mastered_patterns or [])
            if category not in mastered:
                mastered.append(category)
                progress.mastered_patterns = mastered
        else:
            progress.streak = 0
            # Add to weak categories list
            weaks = list(progress.weak_categories or [])
            if category not in weaks:
                weaks.append(category)
                progress.weak_categories = weaks
                
        # Record category usage
        cats = list(progress.prompt_categories_used or [])
        if category not in cats:
            cats.append(category)
            progress.prompt_categories_used = cats

        await db.commit()
        await db.refresh(progress)
        return progress
