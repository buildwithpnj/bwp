from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.task_action_service import TaskActionService

class CreateTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        task = await TaskActionService.create_task(db, user_id, title)
        return {
            "status": "success",
            "task_id": task.id,
            "message": f"Task '{title}' created successfully."
        }
