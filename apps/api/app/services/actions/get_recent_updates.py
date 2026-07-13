from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.action_models import ActionLog

class GetRecentUpdatesAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        limit = payload.get("limit", 10)
        
        stmt = select(ActionLog).where(ActionLog.user_id == user_id).order_by(desc(ActionLog.created_at)).limit(limit)
        res = await db.execute(stmt)
        logs = res.scalars().all()
        
        updates = [f"{log.action_name}: {log.status}" for log in logs]
        return {
            "status": "success",
            "message": "Recent updates compiled.",
            "results": updates
        }
