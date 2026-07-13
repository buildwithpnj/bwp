import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federated_rollback_bundle import FederatedRollbackBundle

class RollbackPreviewService:
    @classmethod
    async def preview_rollback(
        cls,
        db: AsyncSession,
        job_id: str
    ) -> dict:
        """
        Calculates diff snapshots of policies before reversing values.
        """
        stmt = select(FederatedRollbackBundle).where(FederatedRollbackBundle.job_id == job_id)
        res = await db.execute(stmt)
        bundle = res.scalar_one_or_none()
        
        if not bundle:
            raise ValueError("Rollback bundle not found.")
            
        return {
            "job_id": job_id,
            "target_state": json.loads(bundle.snapshot_data)
        }
