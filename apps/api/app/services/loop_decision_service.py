from typing import Any
from app.services.loop_state_store import LoopStateStore

class LoopDecisionService:
    @classmethod
    def evaluate_outcome(cls, state_id: str, budget_service: Any = None) -> str:
        """
        Determines next loop transition by auditing state steps history, confidence trends,
        and budget exhaustions.
        """
        state = LoopStateStore.get_state(state_id)
        if not state:
            return "stop_unknown"
            
        steps = state.get("steps") or []
        if not steps:
            return "continue"

        # 1. Budget check
        if budget_service and not budget_service.has_budget():
            return "stop_budget_exhausted"

        # 2. Confidence collapse check
        from app.llm_settings import llm_settings
        if llm_settings.confidence_collapse_protection:
            confidence = state.get("confidence", 1.0)
            if confidence < 0.4:
                return "stop_confidence_collapse"

        # 3. No-progress check (detect consecutive duplicate actions or queries)
        if llm_settings.no_progress_stop_enabled and len(steps) >= 2:
            last_step = steps[-1]
            prev_step = steps[-2]
            
            # Check if same tool query or same write action is repeated consecutively
            if (
                last_step.get("tool") == prev_step.get("tool") and
                last_step.get("query_or_path") == prev_step.get("query_or_path") and
                last_step.get("tool") in ("search", "read_file", "write_action")
            ):
                return "stop_no_progress"

        # 4. Check if final answer step was appended
        for step in steps:
            if step.get("tool") == "finalize_answer":
                return "success"
                
        # If budget service is not provided, return "success" to support legacy outcomes
        if not budget_service:
            return "success"
            
        return "continue"
