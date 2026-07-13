from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

class CreateSummaryNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success", 
            "message": f"Summary note created for user {user_id}", 
            "summary_id": "sum_abc123"
        }
