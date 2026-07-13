from app.services.loop_state_store import LoopStateStore

class LoopDecisionService:
    @classmethod
    def evaluate_outcome(cls, state_id: str) -> str:
        """
        Determines if the current plan steps achieved goal.
        """
        state = LoopStateStore.get_state(state_id)
        if not state:
            return "unknown"
            
        steps = state.get("steps") or []
        if len(steps) > 0:
            return "success"
        return "insufficient_data"
