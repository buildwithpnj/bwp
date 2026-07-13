from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.policy_sync_job import PolicySyncJob
from app.schemas.policy_sync_request import PolicySyncRequest
from app.services.governance_sync_service import GovernanceSyncService
from app.services.rollback_preview_service import RollbackPreviewService
from app.services.federated_rollback_service import FederatedRollbackService

router = APIRouter(prefix="/api/governance/sync", tags=["Federated Governance Sync"])

@router.post("/preview", status_code=status.HTTP_200_OK)
async def preview_policy_sync(
    source_env: str,
    target_env: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Returns diff comparisons before applying configurations sync.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    # Simulate diff comparing config states
    diff = {"modality_limit": {"old": "25MB", "new": "50MB"}}
    return {
        "source_env": source_env,
        "target_env": target_env,
        "diff": diff,
        "requires_approval": True,
        "drift_detected": True
    }

@router.post("/apply", status_code=status.HTTP_201_CREATED)
async def apply_policy_sync(
    req: PolicySyncRequest,
    current_user: CurrentUser,
    db: DB
):
    """
    Saves and applies configuration changes.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await GovernanceSyncService.process_sync(db, current_user.id, req)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/rollback/preview", status_code=status.HTTP_200_OK)
async def preview_rollback(
    job_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Previews rollback target state before reversing values.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        return await RollbackPreviewService.preview_rollback(db, job_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/rollback/apply", status_code=status.HTTP_200_OK)
async def apply_rollback(
    job_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Reverses configuration changes.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    try:
        state = await FederatedRollbackService.apply_rollback(db, job_id)
        return {
            "status": "rolled_back",
            "restored_state": state
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/jobs", status_code=status.HTTP_200_OK)
async def list_sync_jobs(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists policy sync job logs.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    stmt = select(PolicySyncJob).order_by(PolicySyncJob.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/drift", status_code=status.HTTP_200_OK)
async def list_policy_drift(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists divergent settings configurations.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
        
    return {
        "drift_severity": "low",
        "divergent_keys": ["modality_limit"]
    }
