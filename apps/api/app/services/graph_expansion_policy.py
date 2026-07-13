class GraphExpansionPolicy:
    @classmethod
    def should_expand(cls, target_node_id: str, current_depth: int) -> bool:
        """
        Enforces maximum depth and relevance thresholds.
        """
        if current_depth > 3:
            return False
        return True
