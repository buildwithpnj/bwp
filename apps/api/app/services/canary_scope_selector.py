from typing import List

class CanaryScopeSelector:
    @classmethod
    def filter_canary_targets(cls, all_nodes: List[str], percentage: int) -> List[str]:
        """
        Determines the target nodes to deploy to based on percentage.
        """
        count = max(1, int(len(all_nodes) * (percentage / 100.0)))
        return all_nodes[:count]
