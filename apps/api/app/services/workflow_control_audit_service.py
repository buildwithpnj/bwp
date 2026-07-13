from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
from app.models.workflow_control_event import WorkflowControlEvent

class WorkflowControlAuditService:
    @classmethod
    async def get_audit_summary(cls, db: AsyncSession) -> Dict[str, Any]:
        """
        Aggregates control stats and intervention counts for dashboard metrics.
        """
        # Count by type
        stmt_type = select(
            WorkflowControlEvent.control_type,
            func.count(WorkflowControlEvent.id)
        ).group_by(WorkflowControlEvent.control_type)
        res_type = await db.execute(stmt_type)
        
        by_type = {row[0]: row[1] for row in res_type.all()}
        
        # Count by status
        stmt_status = select(
            WorkflowControlEvent.result_status,
            func.count(WorkflowControlEvent.id)
        ).group_by(WorkflowControlEvent.result_status)
        res_status = await db.execute(stmt_status)
        
        by_status = {row[0]: row[1] for row in res_status.all()}
        
        return {
            "total_interventions": sum(by_status.values()),
            "by_control_type": by_type,
            "by_result_status": by_status
        }
