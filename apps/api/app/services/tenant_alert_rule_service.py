import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant_alert_rule import TenantAlertRule

class TenantAlertRuleService:
    @classmethod
    async def configure_alert_muting(
        cls,
        db: AsyncSession,
        tenant_id: str,
        rule_name: str,
        muted: bool
    ) -> TenantAlertRule:
        """
        Updates threshold rule definitions silencing system warning emails/logs.
        """
        stmt = select(TenantAlertRule).where(
            TenantAlertRule.tenant_id == tenant_id,
            TenantAlertRule.rule_name == rule_name
        )
        res = await db.execute(stmt)
        rule = res.scalar_one_or_none()
        
        if not rule:
            rule = TenantAlertRule(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                rule_name=rule_name,
                is_muted=muted
            )
        else:
            rule.is_muted = muted
            
        db.add(rule)
        await db.commit()
        return rule
        
    @classmethod
    async def is_rule_muted(cls, db: AsyncSession, tenant_id: str, rule_name: str) -> bool:
        """
        Checks if alert rule is muted for this tenant.
        """
        stmt = select(TenantAlertRule).where(
            TenantAlertRule.tenant_id == tenant_id,
            TenantAlertRule.rule_name == rule_name
        )
        res = await db.execute(stmt)
        rule = res.scalar_one_or_none()
        return rule.is_muted if rule else False
