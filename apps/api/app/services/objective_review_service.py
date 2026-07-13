from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.objective_run import ObjectiveRun
from app.models.objective_checkpoint import ObjectiveCheckpoint

class ObjectiveReviewService:
    @classmethod
    async def evaluate_checkpoint(
        cls,
        db: AsyncSession,
        checkpoint_id: str,
        evidence: str
    ) -> bool:
        """
        Gathers evidence to verify if a checkpoint stop condition is achieved.
        """
        stmt = select(ObjectiveCheckpoint).where(ObjectiveCheckpoint.id == checkpoint_id)
        res = await db.execute(stmt)
        cp = res.scalar_one_or_none()
        
        if not cp:
            return False
            
        # If evidence suggests success, mark verified
        if "completed" in evidence.lower() or "success" in evidence.lower():
            cp.status = "verified"
            db.add(cp)
            await db.commit()
            return True
            
        cp.status = "failed"
        db.add(cp)
        await db.commit()
        return False
