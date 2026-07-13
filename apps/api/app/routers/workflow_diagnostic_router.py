from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport
from app.services.workflow_diagnostic_service import WorkflowDiagnosticService

router = APIRouter(prefix="/api/workflows", tags=["Workflow Self-Correction Diagnostics"])

@router.post("/{workflow_id}/diagnose", status_code=status.HTTP_201_CREATED)
async def generate_workflow_diagnostics(
    workflow_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Triggers execution scan diagnostics and recovery suggestions for a failed/degraded workflow run.
    """
    report = await WorkflowDiagnosticService.generate_report(db, workflow_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found or diagnostic parsing failed."
        )
    return report

@router.get("/{workflow_id}/diagnose/latest", status_code=status.HTTP_200_OK)
async def get_latest_diagnostic_report(
    workflow_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Retrieves the most recent diagnostic report card for a workflow run.
    """
    stmt = select(WorkflowDiagnosticReport).where(
        WorkflowDiagnosticReport.workflow_run_id == workflow_id
    ).order_by(WorkflowDiagnosticReport.created_at.desc()).limit(1)
    
    res = await db.execute(stmt)
    report = res.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diagnostic reports found for this workflow run."
        )
        
    return report
