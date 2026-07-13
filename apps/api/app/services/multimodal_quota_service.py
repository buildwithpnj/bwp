from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant_modality_quota import TenantModalityQuota

class MultimodalQuotaService:
    @classmethod
    async def get_or_create_quota(cls, db: AsyncSession, tenant_id: str) -> TenantModalityQuota:
        """
        Retrieves active quota config or provisions a baseline.
        """
        stmt = select(TenantModalityQuota).where(TenantModalityQuota.tenant_id == tenant_id)
        res = await db.execute(stmt)
        quota = res.scalar_one_or_none()
        
        if not quota:
            quota = TenantModalityQuota(
                tenant_id=tenant_id,
                daily_bytes_limit=52428800,  # 50 MB
                daily_bytes_used=0,
                requests_count_limit=100,
                requests_count_used=0
            )
            db.add(quota)
            await db.commit()
            await db.refresh(quota)
        return quota

    @classmethod
    async def consume_quota(cls, db: AsyncSession, tenant_id: str, file_size_bytes: int) -> bool:
        """
        Deducts quota. Returns False if limit is exceeded.
        """
        quota = await cls.get_or_create_quota(db, tenant_id)
        
        if quota.daily_bytes_used + file_size_bytes > quota.daily_bytes_limit:
            return False
        if quota.requests_count_used + 1 > quota.requests_count_limit:
            return False
            
        quota.daily_bytes_used += file_size_bytes
        quota.requests_count_used += 1
        db.add(quota)
        await db.commit()
        return True
