from typing import List, Dict, Any

class SandboxEvaluator:
    @classmethod
    def evaluate_plan_failures(cls, steps: List[Dict[str, Any]]) -> List[str]:
        """
        Heuristically scans steps to detect likely failures (missing details, bad parameters).
        """
        failures = []
        for idx, step in enumerate(steps):
            action = step.get("action_name", "")
            payload = step.get("payload", {})
            
            if action == "create_lesson_note" and not payload.get("content"):
                failures.append(f"Step {idx}: 'content' field in payload cannot be empty.")
            elif action == "build_practice_plan" and not payload.get("focus_area"):
                failures.append(f"Step {idx}: 'focus_area' is required.")
        return failures
