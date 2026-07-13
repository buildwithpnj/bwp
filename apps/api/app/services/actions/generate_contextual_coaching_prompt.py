from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

class GenerateContextualCoachingPromptAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": f"Coaching prompt generated for user {user_id}",
            "prompt_text": "Keep practicing your passive voice usage!"
        }
