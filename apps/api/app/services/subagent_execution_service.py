import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.models.delegation_run import DelegationRun
from app.schemas.delegation_request_schema import DelegationRequest
from app.schemas.delegation_response_schema import DelegationResponse
from app.services.specialist_delegation_policy import SpecialistDelegationPolicy
from app.services.delegation_result_validator import DelegationResultValidator

logger = logging.getLogger("subagent_execution_service")

class SubAgentExecutionService:
    @classmethod
    async def execute_delegation(
        cls,
        db: AsyncSession,
        req: DelegationRequest
    ) -> DelegationResponse:
        """
        Executes a specialist delegation task, logging details and validating responses.
        """
        logger.info(f"Executing subagent delegation: {req.delegation_id} type={req.specialist_type}")
        
        # 1. Increment policy budget spent counters (mock token usage based on agent type)
        token_cost = 1.5 if req.specialist_type == "DatabaseAuditorAgent" else 1.0
        SpecialistDelegationPolicy.increment_counters(token_cost)
        
        # 2. Simulate advisor findings output
        findings = {"anomaly_detected": False, "verified_at": datetime.now(timezone.utc).isoformat()}
        reasoning = f"Specialist subagent review completed for goal: {req.bounded_goal}"
        next_step = {"action": "replay_failed_step"}
        
        if req.specialist_type == "DatabaseAuditorAgent":
            findings["anomaly_detected"] = True
            findings["diagnostics"] = "A foreign key constraint or indexing conflict was found in SQLite schemas."
            reasoning = "Database specialist found SQLite schema foreign key violations."
            next_step = {"action": "escalate_to_admin"}
            
        # 3. Create DelegationResponse
        resp = DelegationResponse(
            delegation_id=req.delegation_id,
            specialist_type=req.specialist_type,
            outcome_status="succeeded",
            reasoning_summary=reasoning,
            structured_findings=findings,
            suggested_next_step=next_step,
            confidence_score=0.95
        )
        
        # 4. Validate output schema
        valid = DelegationResultValidator.validate(resp)
        if not valid:
            resp.outcome_status = "failed"
            resp.reasoning_summary = "Specialist returned invalid schema response."
            
        # 5. Persist run log
        run = DelegationRun(
            id=req.delegation_id,
            workflow_run_id=req.workflow_run_id,
            action_log_id=req.action_log_id,
            parent_step_id=req.parent_step_id,
            requesting_agent=req.requesting_agent,
            specialist_type=req.specialist_type,
            delegation_reason=req.delegation_reason,
            bounded_goal=req.bounded_goal,
            outcome_status=resp.outcome_status,
            reasoning_summary=resp.reasoning_summary,
            structured_findings=resp.structured_findings,
            suggested_next_step=resp.suggested_next_step,
            confidence_score=resp.confidence_score,
            token_cost=token_cost
        )
        db.add(run)
        await db.commit()
        
        return resp
