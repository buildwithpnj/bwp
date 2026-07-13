from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.governance_policy_change import GovernancePolicyChange

class GovernanceAuditService:
    @classmethod
    async def get_revision_history(
        cls,
        db: AsyncSession,
        tenant_id: str
    ) -> List[GovernancePolicyChange]:
        """
        Gathers list of previous tenant settings revisions.
        """
        stmt = select(GovernancePolicyChange).where(
            GovernancePolicyChange.target_tenant_id == tenant_id
        ).order_by(GovernancePolicyChange.created_at.desc())
        
        res = await db.execute(stmt)
        return res.scalars().all()
