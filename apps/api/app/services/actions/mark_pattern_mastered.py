from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.learning_progress_service import LearningProgressService

class MarkPatternMasteredAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Saves grammar patterns to mastered skills array checklist."""
        pattern_name = payload["pattern_name"]
        
        await LearningProgressService.record_correction(db, user_id, pattern_name, was_correct=True)
        
        return {
            "status": "success",
            "message": f"Successfully marked pattern '{pattern_name}' as mastered."
        }
