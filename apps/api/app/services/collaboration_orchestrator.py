import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.collaboration_run import CollaborationRun
from app.schemas.collaboration_request import CollaborationRequest
from app.schemas.collaboration_response import CollaborationResponse
from app.services.handoff_protocol_service import HandoffProtocolService

logger = logging.getLogger("collaboration_orchestrator")

class CollaborationOrchestrator:
    @classmethod
    async def run_collaboration(
        cls,
        db: AsyncSession,
        req: CollaborationRequest
    ) -> CollaborationResponse:
        """
        Orchestrates multi-agent collaboration runs, handling handoffs and merging final results.
        """
        collab_id = str(uuid.uuid4())
        logger.info(f"Initiating collaboration run: {collab_id} with agents {req.participating_agents}")
        
        # 1. Register run
        run = CollaborationRun(
            id=collab_id,
            workflow_run_id=req.workflow_run_id,
            participating_agents=req.participating_agents,
            coordination_status="active",
            max_total_steps=req.max_steps,
            max_parallel_branches=3
        )
        db.add(run)
        await db.commit()
        
        # 2. Drive handoff sequence
        handoffs_count = 0
        tokens = 0.0
        findings = {}
        
        # Iterate over agents and simulate handoffs where pathway allows
        for i in range(len(req.participating_agents) - 1):
            sender = req.participating_agents[i]
            receiver = req.participating_agents[i+1]
            
            payload = {
                "code_findings": "Syntax validation errors found in app/models/finance.py.",
                "database_locks": "Foreign key violations detected.",
                "anomaly_detected": True
            }
            
            success = await HandoffProtocolService.process_handoff(
                db, collab_id, sender, receiver, payload
            )
            
            if success:
                handoffs_count += 1
                tokens += 1.2
                findings[f"{sender}_to_{receiver}"] = "Handoff payload verified and accepted."
            else:
                run.coordination_status = "failed"
                await db.commit()
                return CollaborationResponse(
                    collaboration_id=collab_id,
                    coordination_status="failed",
                    final_merged_result={"error": f"Handoff failed from {sender} to {receiver}."},
                    handoffs_count=handoffs_count,
                    used_tokens=tokens
                )
                
        # 3. Finalize success state and return response
        run.coordination_status = "merged"
        await db.commit()
        
        return CollaborationResponse(
            collaboration_id=collab_id,
            coordination_status="merged",
            final_merged_result={
                "coordination_outcome": "Success",
                "findings_summary": findings
            },
            handoffs_count=handoffs_count,
            used_tokens=tokens
        )
        
    @classmethod
    def enforce_parallel_branch_limit(cls, current_branches_count: int, max_allowed: int = 3) -> bool:
        """
        Helper method to enforce maximum concurrency bounds.
        """
        return current_branches_count <= max_allowed
