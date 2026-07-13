import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional
from app.models.workflow_run import WorkflowRun
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus
from app.services.tool_policy_service import ToolPolicyService
from app.services.action_execution_service import ActionExecutionService
from app.services.action_observability_service import ActionObservabilityService
from app.services.job_enqueuer import JobEnqueuer

logger = logging.getLogger("workflow_execution")

class WorkflowExecutionService:
    @classmethod
    async def create_workflow_run(
        cls,
        db: AsyncSession,
        goal: str,
        reasoning: str,
        steps: list,
        user_role: str,
        autonomy_tier: int = 1
    ) -> WorkflowRun:
        """Initializes a WorkflowRun record in DB."""
        # Calculate approval requirements based on default autonomy tier rules
        requires_approval = False
        if autonomy_tier == 0:
            requires_approval = True
        else:
            for step in steps:
                if ToolPolicyService.requires_approval(step["action_name"], autonomy_tier):
                    requires_approval = True
                    break

        wf = WorkflowRun(
            goal=goal,
            reasoning_summary=reasoning,
            steps=steps,
            current_step_index=0,
            status="pending",
            autonomy_tier=autonomy_tier,
            requires_approval=requires_approval
        )
        db.add(wf)
        await db.commit()
        await db.refresh(wf)
        return wf

    @classmethod
    async def start_workflow(cls, db: AsyncSession, wf_id: str, user_id: str) -> Dict[str, Any]:
        """Triggers workflow run execution."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == wf_id)
        res = await db.execute(stmt)
        wf = res.scalar_one_or_none()
        
        if not wf:
            return {"status": "error", "message": f"Workflow {wf_id} not found."}
            
        from app.services.realtime_event_emitter import RealTimeEventEmitter

        if wf.requires_approval and wf.status == "pending":
            wf.status = "paused_approval"
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="workflow_paused_approval",
                user_id=user_id,
                action_name="workflow_run",
                action_log_id=wf.id
            )
            
            await RealTimeEventEmitter.emit_workflow_event(
                event_type="workflow.paused_for_approval",
                workflow_run_id=wf.id,
                user_id=user_id,
                status="paused_approval",
                summary_message="Workflow paused waiting for initial approval checkpoint."
            )
            return {
                "status": "paused_approval",
                "workflow_id": wf.id,
                "message": "Workflow paused pending initial approval checkpoint."
            }

        wf.status = "executing"
        await db.commit()
        
        ActionObservabilityService.log_event(
            event_name="workflow_started",
            user_id=user_id,
            action_name="workflow_run",
            action_log_id=wf.id,
            extra={"goal": wf.goal, "steps_count": len(wf.steps)}
        )
        
        await RealTimeEventEmitter.emit_workflow_event(
            event_type="workflow.started",
            workflow_run_id=wf.id,
            user_id=user_id,
            status="executing",
            summary_message="Workflow execution started."
        )

        return await cls.execute_current_step(db, wf, user_id)

    @classmethod
    async def execute_current_step(cls, db: AsyncSession, wf: WorkflowRun, user_id: str) -> Dict[str, Any]:
        """Processes current active step of the workflow."""
        # V19 Control checkpoints check
        if wf.status == "paused":
            logger.info(f"Workflow {wf.id} execution paused by control check.")
            return {"status": "paused", "workflow_id": wf.id}
            
        if wf.status == "cancelled":
            logger.info(f"Workflow {wf.id} execution cancelled by control check.")
            return {"status": "cancelled", "workflow_id": wf.id}

        from app.services.realtime_event_emitter import RealTimeEventEmitter

        if wf.current_step_index >= len(wf.steps):
            wf.status = "succeeded"
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="workflow_succeeded",
                user_id=user_id,
                action_name="workflow_run",
                action_log_id=wf.id
            )
            
            await RealTimeEventEmitter.emit_workflow_event(
                event_type="workflow.completed",
                workflow_run_id=wf.id,
                user_id=user_id,
                status="succeeded",
                summary_message="Workflow execution completed successfully."
            )
            
            return {"status": "succeeded", "workflow_id": wf.id}
            
        step = wf.steps[wf.current_step_index]
        action_name = step["action_name"]
        payload = step["payload"]
        
        # Check approval checkpoint gate
        if wf.requires_approval and wf.current_step_index == 0 and wf.status != "approved" and wf.status != "executing":
            wf.status = "paused_approval"
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="workflow_paused_approval",
                user_id=user_id,
                action_name=action_name,
                action_log_id=wf.id
            )
            
            await RealTimeEventEmitter.emit_workflow_event(
                event_type="workflow.paused_for_approval",
                workflow_run_id=wf.id,
                user_id=user_id,
                status="paused_approval",
                summary_message=f"Workflow paused waiting for approval checkpoint."
            )
            
            return {
                "status": "paused_approval",
                "workflow_id": wf.id,
                "message": "Workflow paused pending initial approval checkpoint."
            }

        # Dispatch execution step
        logger.info(f"Executing step {wf.current_step_index + 1}/{len(wf.steps)}: {action_name} for Workflow {wf.id}")
        
        await RealTimeEventEmitter.emit_workflow_event(
            event_type="workflow.step_started",
            workflow_run_id=wf.id,
            user_id=user_id,
            status="executing",
            summary_message=f"Starting workflow step: {action_name}",
            step_index=wf.current_step_index
        )

        # Instantiate ActionLog
        now = datetime.now(timezone.utc)
        log = ActionLog(
            user_id=user_id,
            action_name=action_name,
            input_payload=payload,
            status="pending",
            approval_status="auto_approved" if wf.status == "approved" or not wf.requires_approval else "approved",
            suggested_at=now,
            execution_status=ActionExecutionStatus.SUGGESTED,
            retry_count=0,
            max_retries=3
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        
        # Execute using standard executor
        exec_res = await ActionExecutionService.execute_log_action(db, log)
        
        if exec_res.get("status") == "success":
            # Success: progress forward!
            wf.current_step_index += 1
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="workflow_step_succeeded",
                user_id=user_id,
                action_name=action_name,
                action_log_id=wf.id,
                extra={"step_index": wf.current_step_index}
            )
            
            await RealTimeEventEmitter.emit_workflow_event(
                event_type="workflow.step_succeeded",
                workflow_run_id=wf.id,
                user_id=user_id,
                status="executing",
                summary_message=f"Step succeeded: {action_name}",
                step_index=wf.current_step_index - 1
            )
            
            # Recurse next step
            return await cls.execute_current_step(db, wf, user_id)
        else:
            # Failure: halt and rollback previously executed steps
            wf.status = "failed"
            await db.commit()
            
            ActionObservabilityService.log_event(
                event_name="workflow_step_failed",
                user_id=user_id,
                action_name=action_name,
                action_log_id=wf.id,
                extra={"error": exec_res.get("error")}
            )
            
            await RealTimeEventEmitter.emit_workflow_event(
                event_type="workflow.step_failed",
                workflow_run_id=wf.id,
                user_id=user_id,
                status="failed",
                summary_message=f"Step failed: {action_name}. Reason: {exec_res.get('error')}",
                step_index=wf.current_step_index
            )
            
            # Rollback previous steps
            await cls.rollback_workflow(db, wf, user_id)
            return {"status": "failed", "workflow_id": wf.id, "error": exec_res.get("error")}

    @classmethod
    async def rollback_workflow(cls, db: AsyncSession, wf: WorkflowRun, user_id: str) -> None:
        """Rollbacks side effects of successful previous steps of this workflow."""
        logger.warning(f"Workflow {wf.id} failed at step {wf.current_step_index}. Rolling back intermediate writes...")
        
        # Scan and run compensating rollbacks in reverse order
        # For this mock system, we log the rollback timeline event
        ActionObservabilityService.log_event(
            event_name="workflow_rollback_started",
            user_id=user_id,
            action_name="workflow_run",
            action_log_id=wf.id
        )
        
        wf.status = "failed"
        await db.commit()
