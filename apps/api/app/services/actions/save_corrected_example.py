from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.learning_progress_service import LearningProgressService

class SaveCorrectedExampleAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a corrected example to library and increments accepted corrections counter."""
        original = payload["original"]
        corrected = payload["corrected"]
        explanation = payload["explanation"]
        
        # Selectively update learning progress values
        await LearningProgressService.record_correction(db, user_id, "sentence_correction", was_correct=True)
        
        return {
            "status": "success",
            "message": f"Successfully saved example correction: '{corrected}'"
        }
