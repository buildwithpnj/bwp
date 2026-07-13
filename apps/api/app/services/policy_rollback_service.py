from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.models.delegation_policy_feedback import DelegationPolicyFeedback

class PolicyRollbackService:
    @classmethod
    async def rollback_policy(cls, db: AsyncSession, specialist_type: str, workflow_type: str) -> None:
        """
        Deletes historical policy feedback metrics to restore defaults.
        """
        stmt = delete(DelegationPolicyFeedback).where(
            DelegationPolicyFeedback.specialist_type == specialist_type,
            DelegationPolicyFeedback.workflow_type == workflow_type
        )
        await db.execute(stmt)
        await db.commit()
