from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.memory_action_service import MemoryActionService

class CreateMemoryItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        fact = payload["fact"]
        profile = await MemoryActionService.create_memory_item(db, user_id, fact)
        return {
            "status": "success",
            "message": f"Added fact to memory: '{fact}'"
        }
