from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.deps import CurrentUser, DB
from app.models.action_models import ActionLog
from app.services.action_trace_formatter import ActionTraceFormatter

router = APIRouter(prefix="/api/actions/admin", tags=["Action Admin Dashboard"])

@router.get("/logs", status_code=status.HTTP_200_OK)
async def list_action_logs(
    current_user: CurrentUser,
    db: DB,
    status_filter: Optional[str] = Query(None, alias="status"),
    action_name: Optional[str] = Query(None),
    execution_status: Optional[str] = Query(None),
    recovery_status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Lists historical action execution logs with filters.
    Sanitizes payloads to prevent sensitive data leakage.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )

    stmt = select(ActionLog)
    if status_filter:
        stmt = stmt.where(ActionLog.status == status_filter)
    if action_name:
        stmt = stmt.where(ActionLog.action_name == action_name)
    if execution_status:
        stmt = stmt.where(ActionLog.execution_status == execution_status)
    if recovery_status:
        stmt = stmt.where(ActionLog.recovery_status == recovery_status)

    stmt = stmt.order_by(ActionLog.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    logs = res.scalars().all()

    # Sanitize logs to omit potentially sensitive input/result payloads
    sanitized_logs = []
    for log in logs:
        sanitized_logs.append({
            "id": log.id,
            "user_id": log.user_id,
            "action_name": log.action_name,
            "status": log.status,
            "approval_status": log.approval_status,
            "execution_status": log.execution_status,
            "recovery_status": log.recovery_status,
            "suggested_at": log.suggested_at.isoformat() if log.suggested_at else None,
            "approved_at": log.approved_at.isoformat() if log.approved_at else None,
            "queued_at": log.queued_at.isoformat() if log.queued_at else None,
            "execution_started_at": log.execution_started_at.isoformat() if log.execution_started_at else None,
            "executed_at": log.executed_at.isoformat() if log.executed_at else None,
            "failed_at": log.failed_at.isoformat() if log.failed_at else None,
            "rolled_back_at": log.rolled_back_at.isoformat() if log.rolled_back_at else None,
            "retry_count": log.retry_count,
            "max_retries": log.max_retries,
            "last_error": log.last_error,
            "idempotency_key": log.idempotency_key
        })

    return sanitized_logs

@router.get("/trace/{log_id}", status_code=status.HTTP_200_OK)
async def get_action_trace(
    log_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Returns a human-readable execution trace timeline for a given action log ID.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )

    stmt = select(ActionLog).where(ActionLog.id == log_id)
    res = await db.execute(stmt)
    log = res.scalar_one_or_none()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action log not found."
        )

    trace_text = ActionTraceFormatter.format_trace(log)
    return {"trace": trace_text}
