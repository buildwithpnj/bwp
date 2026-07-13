from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.objective_checkpoint import ObjectiveCheckpoint
from app.models.objective_run import ObjectiveRun

class ObjectiveProgressService:
    @classmethod
    async def update_objective_progress(cls, db: AsyncSession, objective_run_id: str) -> float:
        """
        Recomputes percentage based on completed checkpoints.
        """
        # Count all checkpoints
        stmt_total = select(func.count(ObjectiveCheckpoint.id)).where(
            ObjectiveCheckpoint.objective_run_id == objective_run_id
        )
        total_res = await db.execute(stmt_total)
        total = total_res.scalar() or 0
        
        if total == 0:
            return 0.0
            
        stmt_verified = select(func.count(ObjectiveCheckpoint.id)).where(
            ObjectiveCheckpoint.objective_run_id == objective_run_id,
            ObjectiveCheckpoint.status == "verified"
        )
        ver_res = await db.execute(stmt_verified)
        verified = ver_res.scalar() or 0
        
        progress = (verified / total) * 100.0
        
        # Update run model
        stmt_run = select(ObjectiveRun).where(ObjectiveRun.id == objective_run_id)
        run_res = await db.execute(stmt_run)
        run = run_res.scalar_one_or_none()
        if run:
            run.progress_percent = progress
            db.add(run)
            await db.commit()
            
        return progress
