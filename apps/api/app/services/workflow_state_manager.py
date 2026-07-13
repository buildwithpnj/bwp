import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
from app.models.workflow_run import WorkflowRun
from app.services.workflow_execution_service import WorkflowExecutionService

logger = logging.getLogger("workflow_state_manager")

class WorkflowStateManager:
    @classmethod
    async def approve_and_resume(cls, db: AsyncSession, wf_id: str, user_id: str) -> Dict[str, Any]:
        """Approves a paused workflow and triggers execution resumption."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == wf_id)
        res = await db.execute(stmt)
        wf = res.scalar_one_or_none()
        
        if not wf:
            return {"status": "error", "message": f"Workflow {wf_id} not found."}
            
        if wf.status != "paused_approval":
            return {"status": "error", "message": f"Workflow {wf_id} is not waiting for approval."}
            
        logger.info(f"Workflow {wf_id} approved. Resuming execution flow...")
        wf.status = "approved"
        await db.commit()
        
        # Drive steps forward
        return await WorkflowExecutionService.execute_current_step(db, wf, user_id)
