class RetrievalLatencyTracker:
    @classmethod
    def evaluate_timing(cls, latency_ms: float) -> str:
        """
        Grades retrieval times against maximum budget allocations.
        """
        if latency_ms < 50.0:
            return "excellent"
        elif latency_ms < 150.0:
            return "acceptable"
        return "slow"
