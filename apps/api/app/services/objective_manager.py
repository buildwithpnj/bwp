import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.objective_run import ObjectiveRun
from app.models.objective_checkpoint import ObjectiveCheckpoint
from app.schemas.objective_schema import ObjectiveCreate

class ObjectiveManager:
    @classmethod
    async def create_objective(
        cls,
        db: AsyncSession,
        user_id: str,
        data: ObjectiveCreate
    ) -> ObjectiveRun:
        """
        Creates a new long-horizon user objective and schedules base verification checkpoints.
        """
        obj_id = str(uuid.uuid4())
        obj = ObjectiveRun(
            id=obj_id,
            user_id=user_id,
            title=data.title,
            description=data.description,
            progress_percent=0.0,
            status="active",
            stop_condition=data.stop_condition
        )
        db.add(obj)
        
        # Provision initial verification checkpoint
        checkpoint = ObjectiveCheckpoint(
            id=str(uuid.uuid4()),
            objective_run_id=obj_id,
            title="Baseline verification",
            status="pending"
        )
        db.add(checkpoint)
        
        await db.commit()
        await db.refresh(obj)
        return obj
