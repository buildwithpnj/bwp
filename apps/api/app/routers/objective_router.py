from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.schemas.objective_schema import ObjectiveCreate
from app.models.objective_run import ObjectiveRun
from app.services.objective_manager import ObjectiveManager

router = APIRouter(prefix="/api/objectives", tags=["Long-Horizon Goals"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_goal_objective(
    req: ObjectiveCreate,
    current_user: CurrentUser,
    db: DB
):
    """
    Provisions a new long-horizon user objective run and schedules initial verification checkpoints.
    """
    obj = await ObjectiveManager.create_objective(db, current_user.id, req)
    return {
        "id": obj.id,
        "title": obj.title,
        "progress_percent": obj.progress_percent,
        "status": obj.status
    }

@router.get("", status_code=status.HTTP_200_OK)
async def list_active_objectives(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists active objectives for the current user session context.
    """
    stmt = select(ObjectiveRun).where(ObjectiveRun.user_id == current_user.id)
    res = await db.execute(stmt)
    runs = res.scalars().all()
    return [{
        "id": r.id,
        "title": r.title,
        "progress_percent": r.progress_percent,
        "status": r.status
    } for r in runs]
