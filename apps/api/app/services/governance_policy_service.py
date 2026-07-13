import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance_policy_change import GovernancePolicyChange
from app.schemas.governance_update_request import GovernanceUpdateRequest

class GovernancePolicyService:
    @classmethod
    async def log_policy_change(
        cls,
        db: AsyncSession,
        user_id: str,
        data: GovernanceUpdateRequest,
        old_val: str
    ) -> GovernancePolicyChange:
        """
        Records a policy modification in audit trails for rollback and safety guarantees.
        """
        change = GovernancePolicyChange(
            id=str(uuid.uuid4()),
            changed_by_user_id=user_id,
            target_tenant_id=data.tenant_id,
            field_name=data.field_name,
            old_value=old_val,
            new_value=data.new_value
        )
        db.add(change)
        await db.commit()
        return change
