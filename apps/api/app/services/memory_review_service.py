from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_profile_memory_service import UserProfileMemoryService
from app.services.memory_write_policy import MemoryWritePolicy
from app.models.governance import AdminAuditLog
from typing import Dict, Any

class MemoryReviewService:
    @classmethod
    async def review_and_update_profile(
        cls, 
        db: AsyncSession, 
        user_id: str, 
        user_role: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """Processes personalization memory update request evaluating safety write policies."""
        if not MemoryWritePolicy.can_write_profile(user_role, updates):
            return False
            
        await UserProfileMemoryService.update_profile(db, user_id, updates)
        
        # Log auditable action of memory updates
        log = AdminAuditLog(
            admin_id=user_id,
            action="update_personalization_memory",
            details=f"Updated personalization settings: {list(updates.keys())}"
        )
        db.add(log)
        await db.commit()
        return True
