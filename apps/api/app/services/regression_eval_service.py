from typing import List, Dict, Any

class RegressionEvalService:
    @classmethod
    def check_for_preventable_failures(
        cls,
        steps: List[Dict[str, Any]],
        historical_failures: List[str]
    ) -> List[str]:
        """
        Scans steps against historical regression signatures to catch repeated pitfalls.
        """
        preventable = []
        for step in steps:
            action = step.get("action_name", "")
            if action in historical_failures:
                preventable.append(f"Action '{action}' historically triggers high fail rates.")
        return preventable
