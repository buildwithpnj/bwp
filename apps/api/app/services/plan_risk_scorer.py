from typing import List, Dict, Any

class PlanRiskScorer:
    @classmethod
    def calculate_plan_risk(cls, steps: List[Dict[str, Any]]) -> float:
        """
        Rates plan risk level based on action policy tiers.
        """
        max_risk = 0.0
        for step in steps:
            action = step.get("action_name", "")
            # High risk actions
            if action in ["delete_account", "transfer_funds", "drop_table"]:
                max_risk = max(max_risk, 0.9)
            elif action in ["build_practice_plan", "execute_delegation"]:
                max_risk = max(max_risk, 0.4)
            else:
                max_risk = max(max_risk, 0.1)
        return max_risk
