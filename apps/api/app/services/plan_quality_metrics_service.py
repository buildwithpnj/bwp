from typing import List, Dict, Any

class PlanQualityMetricsService:
    @classmethod
    def analyze_steps_metrics(cls, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Gathers count stats on steps types.
        """
        return {
            "total_steps": len(steps),
            "contains_delegations": any(s.get("action_name") == "execute_delegation" for s in steps)
        }
