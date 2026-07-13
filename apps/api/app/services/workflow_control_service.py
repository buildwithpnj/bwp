import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.workflow_run import WorkflowRun
from app.models.workflow_control_event import WorkflowControlEvent
from app.schemas.workflow_control_request import WorkflowControlRequest
from app.schemas.workflow_control_result import WorkflowControlResult
from app.services.workflow_execution_service import WorkflowExecutionService
from app.services.realtime_event_emitter import RealTimeEventEmitter

logger = logging.getLogger("workflow_control_service")

class WorkflowControlService:
    @classmethod
    async def apply_control(
        cls,
        db: AsyncSession,
        workflow_run_id: str,
        req: WorkflowControlRequest,
        user_id: str,
        user_role: str
    ) -> WorkflowControlResult:
        """
        Validates, applies, and audits human-in-the-loop control operations on active workflows.
        """
        now = datetime.now(timezone.utc)
        
        # Load WorkflowRun
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        res = await db.execute(stmt)
        wf = res.scalar_one_or_none()
        
        if not wf:
            return WorkflowControlResult(
                workflow_run_id=workflow_run_id,
                applied_at=now,
                result_status="error",
                message=f"Workflow run {workflow_run_id} not found."
            )
            
        # Admin gating checks
        if req.control_type == "force_recovery_review" and user_role != "internal_admin":
            return WorkflowControlResult(
                workflow_run_id=workflow_run_id,
                applied_at=now,
                result_status="rejected",
                message="Role unauthorized to trigger manual recovery review."
            )
            
        # Execute Control Operations
        result_status = "applied"
        msg = "Control applied successfully."
        
        if req.control_type == "pause_workflow":
            if wf.status != "executing":
                result_status = "rejected"
                msg = f"Cannot pause: workflow is in state '{wf.status}'."
            else:
                wf.status = "paused"
                await db.commit()
                await RealTimeEventEmitter.emit_workflow_event(
                    event_type="workflow.paused",
                    workflow_run_id=wf.id,
                    user_id=user_id,
                    status="paused",
                    summary_message="Workflow paused by user request."
                )
                
        elif req.control_type == "resume_workflow":
            if wf.status != "paused":
                result_status = "rejected"
                msg = f"Cannot resume: workflow is in state '{wf.status}'."
            else:
                wf.status = "executing"
                await db.commit()
                await RealTimeEventEmitter.emit_workflow_event(
                    event_type="workflow.resumed",
                    workflow_run_id=wf.id,
                    user_id=user_id,
                    status="executing",
                    summary_message="Workflow resumed by user."
                )
                # Resumes execution
                await WorkflowExecutionService.execute_current_step(db, wf, user_id)
                
        elif req.control_type == "cancel_workflow":
            if wf.status in ["succeeded", "failed", "cancelled"]:
                result_status = "rejected"
                msg = f"Cannot cancel: workflow is already '{wf.status}'."
            else:
                wf.status = "cancelled"
                await db.commit()
                await RealTimeEventEmitter.emit_workflow_event(
                    event_type="workflow.cancelled",
                    workflow_run_id=wf.id,
                    user_id=user_id,
                    status="cancelled",
                    summary_message="Workflow cancelled."
                )
                await WorkflowExecutionService.rollback_workflow(db, wf, user_id)
                
        elif req.control_type == "replay_failed_step":
            if wf.status != "failed":
                result_status = "rejected"
                msg = f"Cannot replay: workflow is in state '{wf.status}'."
            else:
                target_idx = req.step_index if req.step_index is not None else wf.current_step_index
                if target_idx < 0 or target_idx >= len(wf.steps):
                    result_status = "rejected"
                    msg = "Invalid step index specified for replay."
                else:
                    logger.info(f"Replaying failed workflow step {target_idx}")
                    wf.current_step_index = target_idx
                    wf.status = "executing"
                    await db.commit()
                    await RealTimeEventEmitter.emit_workflow_event(
                        event_type="workflow.step_started",
                        workflow_run_id=wf.id,
                        user_id=user_id,
                        status="executing",
                        summary_message=f"Replaying step index {target_idx}.",
                        step_index=target_idx
                    )
                    await WorkflowExecutionService.execute_current_step(db, wf, user_id)
        else:
            result_status = "rejected"
            msg = f"Unknown control operation type '{req.control_type}'."

        # Log audit trial control event record
        event = WorkflowControlEvent(
            workflow_run_id=workflow_run_id,
            control_type=req.control_type,
            requested_by_user_id=user_id,
            requested_by_role=user_role,
            reason=req.reason,
            applied_at=now,
            result_status=result_status
        )
        db.add(event)
        await db.commit()
        
        return WorkflowControlResult(
            workflow_run_id=workflow_run_id,
            applied_at=now,
            result_status=result_status,
            message=msg
        )
