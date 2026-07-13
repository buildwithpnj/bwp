class AnomalyDedupService:
    @classmethod
    def is_duplicate(cls, active_keys: list, current_key: str) -> bool:
        """
        Suppresses low-value alerts if key exists.
        """
        return current_key in active_keys
