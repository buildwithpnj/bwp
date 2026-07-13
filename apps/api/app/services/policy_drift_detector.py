from typing import Dict, Any

class PolicyDriftDetector:
    @classmethod
    def detect_drift(cls, source_state: Dict[str, Any], target_state: Dict[str, Any]) -> bool:
        """
        Returns True if any configurations diverged or drift from source base.
        """
        for k, v in source_state.items():
            if target_state.get(k) != v:
                return True
        return False
