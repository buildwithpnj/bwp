from typing import Dict, Any

class PolicyDiffService:
    @classmethod
    def compute_diff(cls, source_state: Dict[str, Any], target_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Computes structured field differences.
        """
        diff = {}
        for k, v in source_state.items():
            t_val = target_state.get(k)
            if t_val != v:
                diff[k] = {"old": t_val, "new": v}
        return diff
