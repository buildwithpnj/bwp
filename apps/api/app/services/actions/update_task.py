from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.task_action_service import TaskActionService

class UpdateTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        status = payload["status"]
        
        # Verify ownership
        task = await TaskActionService.get_task(db, task_id)
        if not task or task.user_id != user_id:
            return {"status": "failed", "error": "Task not found or unauthorized access."}
            
        progress = 100 if status == "completed" else 50
        updated = await TaskActionService.update_task_status(db, task_id, status, progress)
        return {
            "status": "success",
            "task_id": updated.id,
            "message": f"Task '{updated.title}' updated to '{status}'."
        }
