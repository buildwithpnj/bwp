from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.project_action_service import ProjectActionService

class UpdateProjectItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        project_id = payload["project_id"]
        status = payload["status"]
        
        project = await ProjectActionService.get_project_item(db, project_id)
        if not project or project.user_id != user_id:
            return {"status": "failed", "error": "Project item not found or unauthorized access."}
            
        updated = await ProjectActionService.update_project_item_status(db, project_id, status)
        return {
            "status": "success",
            "project_id": updated.id,
            "message": f"Project item '{updated.name}' status updated to '{status}'."
        }
