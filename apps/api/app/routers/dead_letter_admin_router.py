from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from app.deps import CurrentUser, DB
from app.services.dead_letter_service import DeadLetterService

router = APIRouter(prefix="/api/actions/admin/dlq", tags=["Action Admin DLQ Management"])

@router.get("", status_code=status.HTTP_200_OK)
async def list_dlq_jobs(
    current_user: CurrentUser,
    db: DB,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Lists permanently failed or dead-lettered action jobs.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )
        
    logs = await DeadLetterService.list_dlq_logs(db, limit, offset)
    
    # Sanitize payload leakage
    return [{
        "id": log.id,
        "user_id": log.user_id,
        "action_name": log.action_name,
        "status": log.status,
        "execution_status": log.execution_status,
        "retry_count": log.retry_count,
        "last_error": log.last_error,
        "dead_lettered_at": log.dead_lettered_at.isoformat() if log.dead_lettered_at else None
    } for log in logs]

@router.post("/replay/{log_id}", status_code=status.HTTP_200_OK)
async def replay_dlq_job(
    log_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Manually triggers execution retry for a dead-lettered log.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )
        
    success = await DeadLetterService.replay_dlq_job(db, log_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Replay failed. Action log may not be dead-lettered."
        )
        
    return {"status": "success", "message": f"Successfully replayed action log {log_id}"}
