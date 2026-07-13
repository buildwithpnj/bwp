from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional
from app.models.workflow_run import WorkflowRun

class RealTimeResyncService:
    @classmethod
    async def get_workflow_sync_state(
        cls,
        db: AsyncSession,
        workflow_run_id: str,
        client_last_step_index: int
    ) -> Dict[str, Any]:
        """
        Calculates status changes or missing workflow executions since the client last synced.
        """
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        res = await db.execute(stmt)
        wf = res.scalar_one_or_none()
        
        if not wf:
            return {"status": "error", "message": "Workflow not found"}
            
        missed_steps = []
        if wf.current_step_index > client_last_step_index:
            # Gather steps completed since client lost connection
            missed_steps = wf.steps[client_last_step_index:wf.current_step_index]
            
        return {
            "status": wf.status,
            "current_step_index": wf.current_step_index,
            "missed_steps": missed_steps,
            "goal": wf.goal
        }
