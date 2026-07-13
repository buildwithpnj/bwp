import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant_agent_policy import TenantAgentPolicy

class TenantAgentConfigService:
    @classmethod
    async def configure_agent_availability(
        cls,
        db: AsyncSession,
        tenant_id: str,
        agent_type: str,
        enabled: bool
    ) -> TenantAgentPolicy:
        """
        Updates agent capabilities status per tenant limits.
        """
        stmt = select(TenantAgentPolicy).where(
            TenantAgentPolicy.tenant_id == tenant_id,
            TenantAgentPolicy.agent_type == agent_type
        )
        res = await db.execute(stmt)
        policy = res.scalar_one_or_none()
        
        if not policy:
            policy = TenantAgentPolicy(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                agent_type=agent_type,
                is_enabled=enabled
            )
        else:
            policy.is_enabled = enabled
            
        db.add(policy)
        await db.commit()
        return policy
