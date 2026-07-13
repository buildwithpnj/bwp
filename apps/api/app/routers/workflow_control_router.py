from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List
from app.deps import CurrentUser, DB
from app.schemas.workflow_control_request import WorkflowControlRequest
from app.schemas.workflow_control_result import WorkflowControlResult
from app.services.workflow_control_service import WorkflowControlService
from app.services.workflow_control_audit_service import WorkflowControlAuditService

router = APIRouter(prefix="/api/workflows", tags=["Workflow Control Plane"])

@router.post("/{workflow_id}/control", response_model=WorkflowControlResult, status_code=status.HTTP_200_OK)
async def apply_workflow_control(
    workflow_id: str,
    req: WorkflowControlRequest,
    current_user: CurrentUser,
    db: DB
):
    """
    Applies a control command (pause, resume, cancel, replay) on a target workflow run.
    """
    res = await WorkflowControlService.apply_control(
        db=db,
        workflow_run_id=workflow_id,
        req=req,
        user_id=current_user.id,
        user_role=current_user.role
    )
    
    if res.result_status == "rejected":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.message
        )
    elif res.result_status == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=res.message
        )
        
    return res

@router.get("/admin/controls/audit", status_code=status.HTTP_200_OK)
async def get_workflow_interventions_audit(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns summary statistics for human workflow control interventions.
    Only accessible by internal_admin users.
    """
    if current_user.role != "internal_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admin users."
        )
        
    summary = await WorkflowControlAuditService.get_audit_summary(db)
    return summary
