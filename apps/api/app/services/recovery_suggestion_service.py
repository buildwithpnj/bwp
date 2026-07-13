from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.workflow_run import WorkflowRun
from app.models.action_models import ActionLog
from app.schemas.recovery_plan import RecoveryOption
from app.services.recovery_policy_service import RecoveryPolicyService
from app.services.recovery_option_ranker import RecoveryOptionRanker

class RecoverySuggestionService:
    @classmethod
    async def generate_and_rank_suggestions(
        cls,
        db: AsyncSession,
        wf: WorkflowRun,
        log: ActionLog,
        patterns: List[str]
    ) -> List[RecoveryOption]:
        """
        Generates and ranks a set of context-specific workflow recovery options.
        """
        options = []
        
        # 1. Base case: standard step failure
        if "repeated_retry_pattern" in patterns:
            # High severity: retry threshold hit
            options.append(
                RecoveryPolicyService.evaluate_option(
                    action_type="cancel_workflow",
                    description="Cancel execution immediately and clean up partial state.",
                    parameters={"workflow_run_id": wf.id}
                )
            )
            options.append(
                RecoveryPolicyService.evaluate_option(
                    action_type="escalate_to_admin",
                    description="Flag workflow run for manual internal_admin inspection.",
                    parameters={"workflow_run_id": wf.id, "reason": "Max retries hit"}
                )
            )
        else:
            # Normal single failure: suggest replay
            options.append(
                RecoveryPolicyService.evaluate_option(
                    action_type="replay_failed_step",
                    description="Replay the failed step from the last successful checkpoint.",
                    parameters={"workflow_run_id": wf.id, "step_index": wf.current_step_index}
                )
            )
            options.append(
                RecoveryPolicyService.evaluate_option(
                    action_type="cancel_workflow",
                    description="Cancel execution immediately.",
                    parameters={"workflow_run_id": wf.id}
                )
            )
            
        return RecoveryOptionRanker.rank_options(options)
