from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.canary_rollout import CanaryRollout
from app.schemas.release_plan_schema import ReleasePlanCreate
from app.services.canary_rollout_service import CanaryRolloutService
from app.services.release_approval_service import ReleaseApprovalService
from app.services.rollout_stage_manager import RolloutStageManager
from app.services.rollout_health_service import RolloutHealthService

router = APIRouter(prefix="/api/releases", tags=["Canary Rollouts & Safe Deployments"])

@router.post("/plan", status_code=status.HTTP_201_CREATED)
async def create_release_plan(
    data: ReleasePlanCreate,
    current_user: CurrentUser,
    db: DB
):
    """
    Saves and initiates a gradual release rollout schedule.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await CanaryRolloutService.initiate_rollout(db, data.rollout_id, data.canary_percentage)

@router.post("/approve", status_code=status.HTTP_200_OK)
async def approve_release(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Registers approval to pass gating checks.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await ReleaseApprovalService.approve_release(db, rollout_id, current_user.id)

@router.post("/canary/start", status_code=status.HTTP_200_OK)
async def start_canary(
    rollout_id: str,
    percentage: int,
    current_user: CurrentUser,
    db: DB
):
    """
    Adjusts active canary percentage.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await CanaryRolloutService.update_percentage(db, rollout_id, percentage)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/canary/pause", status_code=status.HTTP_200_OK)
async def pause_canary(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Pauses canary progression.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await RolloutStageManager.modify_rollout_status(db, rollout_id, "pause")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/canary/resume", status_code=status.HTTP_200_OK)
async def resume_canary(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Resumes paused canary rollout progression.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await RolloutStageManager.modify_rollout_status(db, rollout_id, "resume")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/canary/rollback", status_code=status.HTTP_200_OK)
async def trigger_canary_rollback(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Aborts rollout and initiates rollback.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await RolloutStageManager.modify_rollout_status(db, rollout_id, "rollback")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/status", status_code=status.HTTP_200_OK)
async def get_rollout_status(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Gets release status detail parameters.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(CanaryRollout).where(CanaryRollout.rollout_id == rollout_id)
    res = await db.execute(stmt)
    canary = res.scalar_one_or_none()
    if not canary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rollout not found."
        )
    return canary

@router.get("/health", status_code=status.HTTP_200_OK)
async def check_rollout_health(
    rollout_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Scores and records health checks delta snapshots.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return await RolloutHealthService.measure_health(db, rollout_id, 0.01, 120.0)
