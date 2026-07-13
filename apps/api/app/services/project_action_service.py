import logging
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project_item import ProjectItem
from typing import Dict, Any, List, Optional

logger = logging.getLogger("project_action_service")

class ProjectActionService:
    @classmethod
    async def create_project_item(
        cls,
        db: AsyncSession,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        status: str = "active"
    ) -> ProjectItem:
        """
        Creates a new project item tracking record.
        """
        project_item = ProjectItem(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            description=description,
            status=status
        )
        db.add(project_item)
        await db.commit()
        await db.refresh(project_item)
        logger.info(f"Created project item: {project_item.id} for user: {user_id}")
        return project_item

    @classmethod
    async def get_project_item(cls, db: AsyncSession, project_item_id: str) -> Optional[ProjectItem]:
        stmt = select(ProjectItem).where(ProjectItem.id == project_item_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def update_project_item_status(
        cls,
        db: AsyncSession,
        project_item_id: str,
        status: str
    ) -> Optional[ProjectItem]:
        """
        Updates project item status.
        """
        project_item = await cls.get_project_item(db, project_item_id)
        if not project_item:
            return None
            
        project_item.status = status
        db.add(project_item)
        await db.commit()
        await db.refresh(project_item)
        logger.info(f"Updated project item: {project_item_id} status to {status}")
        return project_item
