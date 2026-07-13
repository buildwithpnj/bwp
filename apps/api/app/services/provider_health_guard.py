class ProviderHealthGuard:
    @classmethod
    def evaluate_provider_health(cls, error_rate: float, latency: float) -> str:
        """
        Assesses downstream model vendor health status.
        """
        if error_rate > 0.25 or latency > 5000.0:
            return "critical"
        elif error_rate > 0.10:
            return "degraded"
        return "healthy"
