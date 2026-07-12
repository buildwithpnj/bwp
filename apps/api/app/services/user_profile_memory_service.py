from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_profile_memory import UserProfileMemory
from typing import Dict, Any, Optional

class UserProfileMemoryService:
    @classmethod
    async def get_or_create_profile(cls, db: AsyncSession, user_id: str) -> UserProfileMemory:
        result = await db.execute(select(UserProfileMemory).where(UserProfileMemory.user_id == user_id))
        profile = result.scalar_one_or_none()
        if not profile:
            profile = UserProfileMemory(
                user_id=user_id,
                tone="professional",
                explanation_style="detailed",
                target_english_level="Advanced",
                weaknesses=[],
                goals=[],
                preferred_language="English"
            )
            db.add(profile)
            await db.commit()
            await db.refresh(profile)
        return profile

    @classmethod
    async def update_profile(cls, db: AsyncSession, user_id: str, updates: Dict[str, Any]) -> UserProfileMemory:
        profile = await cls.get_or_create_profile(db, user_id)
        
        allowed_keys = ["tone", "explanation_style", "target_english_level", "weaknesses", "goals", "preferred_language"]
        for key, value in updates.items():
            if key in allowed_keys:
                setattr(profile, key, value)
                
        await db.commit()
        await db.refresh(profile)
        return profile
