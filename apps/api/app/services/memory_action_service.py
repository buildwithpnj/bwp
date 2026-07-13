import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_memory_service import UserMemoryService
from app.models.user_profile_memory import UserProfileMemory

logger = logging.getLogger("memory_action_service")

class MemoryActionService:
    @classmethod
    async def create_memory_item(
        cls,
        db: AsyncSession,
        user_id: str,
        fact: str
    ) -> UserProfileMemory:
        """
        Adds a new fact to the user's profile memory goals/facts list.
        """
        profile = await UserMemoryService.get_profile(db, user_id)
        
        current_goals = list(profile.goals) if profile.goals else []
        if fact not in current_goals:
            current_goals.append(fact)
            
        # Update profile memory
        profile.goals = current_goals
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        logger.info(f"Added fact to memory for user: {user_id}: '{fact}'")
        return profile
