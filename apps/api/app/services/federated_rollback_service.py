import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federated_rollback_bundle import FederatedRollbackBundle

class FederatedRollbackService:
    @classmethod
    async def apply_rollback(
        cls,
        db: AsyncSession,
        job_id: str
    ) -> dict:
        """
        Reverses configurations changes using snapshot snapshots.
        """
        stmt = select(FederatedRollbackBundle).where(FederatedRollbackBundle.job_id == job_id)
        res = await db.execute(stmt)
        bundle = res.scalar_one_or_none()
        
        if not bundle:
            raise ValueError("Rollback bundle not found.")
            
        restored_state = json.loads(bundle.snapshot_data)
        
        # In a real environment, restore state across nodes
        return restored_state
