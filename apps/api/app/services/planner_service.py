from typing import List, Dict, Any

class PlannerService:
    @classmethod
    def plan_task(cls, prompt: str) -> List[Dict[str, Any]]:
        """
        Decomposes complex requests into steps list.
        """
        # simple keyword decomposition
        if "sync" in prompt.lower():
            return [
                {"step_index": 1, "tool": "search", "query": "sync configuration settings"},
                {"step_index": 2, "tool": "read_file", "path": "docs/v35_governance_sync.md"}
            ]
        return [
            {"step_index": 1, "tool": "search", "query": prompt}
        ]
