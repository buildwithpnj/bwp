from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.services.project_action_service import ProjectActionService

class CreateProjectItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = payload["name"]
        project = await ProjectActionService.create_project_item(db, user_id, name)
        return {
            "status": "success",
            "project_id": project.id,
            "message": f"Project item '{name}' created successfully."
        }
