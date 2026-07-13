class DelayPolicy:
    @classmethod
    def calculate_delay(cls, retry_count: int, base_delay: int = 2) -> int:
        """
        Calculates exponential backoff delay: base_delay * (2 ** retry_count).
        """
        return base_delay * (2 ** retry_count)
