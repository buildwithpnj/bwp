from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.user_profile_memory_service import UserProfileMemoryService

class UpdatePreferenceAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Saves user tone, explanation style, target level preferences updates."""
        updates = {
            "tone": payload["tone"],
            "explanation_style": payload["explanation_style"]
        }
        
        await UserProfileMemoryService.update_profile(db, user_id, updates)
        
        return {
            "status": "success",
            "message": f"Successfully updated preferences: tone={payload['tone']}, style={payload['explanation_style']}"
        }
