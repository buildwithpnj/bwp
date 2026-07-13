from typing import Dict, Any
from app.services.loop_orchestrator import LoopOrchestrator
from app.services.loop_health_service import LoopHealthService
from app.services.run_trace_service import RunTraceService
from app.services.finalization_policy_service import FinalizationPolicyService

class FullLoopRuntime:
    @classmethod
    def execute_full_run(cls, prompt: str, tenant_id: str) -> Dict[str, Any]:
        """
        Coordinates full plan-retrieve-reflect-act looping routines.
        """
        res = LoopOrchestrator.execute_loop(prompt, tenant_id)
        state_id = res["state_id"]
        
        # Calculate health metrics
        health = LoopHealthService.calculate_health(state_id)
        
        # Save run trace log
        RunTraceService.save_trace(state_id, health)
        
        # Finalize response
        final_answer = FinalizationPolicyService.compile_final(state_id)
        
        return {
            "state_id": state_id,
            "final_answer": final_answer,
            "health_metrics": health
        }
