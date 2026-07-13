from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.actions.update_task import UpdateTaskAction

class CompleteTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        return await UpdateTaskAction.execute(db, user_id, {"task_id": task_id, "status": "completed"})
