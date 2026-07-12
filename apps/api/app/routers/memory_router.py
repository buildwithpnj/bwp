from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import DB, CurrentUser
from app.services.user_profile_memory_service import UserProfileMemoryService
from app.services.learning_progress_service import LearningProgressService
from app.services.memory_review_service import MemoryReviewService
from typing import Dict, Any, Optional, List

router = APIRouter(prefix="/api/memory", tags=["Personalization Memory"])

class UpdateProfileSchema(BaseModel):
    tone: Optional[str] = "professional"
    explanation_style: Optional[str] = "detailed"
    target_english_level: Optional[str] = "Advanced"
    preferred_language: Optional[str] = "English"
    weaknesses: Optional[List[str]] = None
    goals: Optional[List[str]] = None

@router.get("/profile")
async def get_profile(current_user: CurrentUser, db: DB):
    profile = await UserProfileMemoryService.get_or_create_profile(db, current_user.id)
    return {
        "tone": profile.tone,
        "explanation_style": profile.explanation_style,
        "target_english_level": profile.target_english_level,
        "preferred_language": profile.preferred_language,
        "weaknesses": profile.weaknesses or [],
        "goals": profile.goals or []
    }

@router.post("/profile")
async def update_profile(updates: UpdateProfileSchema, current_user: CurrentUser, db: DB):
    payload = updates.model_dump(exclude_unset=True)
    success = await MemoryReviewService.review_and_update_profile(
        db, user_id=current_user.id, user_role=current_user.role, updates=payload
    )
    if not success:
        raise HTTPException(status_code=400, detail="Personalization update rejected by safety policy.")
    return {"status": "updated"}

@router.get("/progress")
async def get_progress(current_user: CurrentUser, db: DB):
    progress = await LearningProgressService.get_or_create_progress(db, current_user.id)
    return {
        "corrections_accepted": progress.corrections_accepted,
        "streak": progress.streak,
        "mastered_patterns": progress.mastered_patterns or [],
        "weak_categories": progress.weak_categories or [],
        "prompt_categories_used": progress.prompt_categories_used or []
    }
