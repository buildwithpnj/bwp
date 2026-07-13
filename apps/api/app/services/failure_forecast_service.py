class FailureForecastService:
    @classmethod
    def forecast_failure_probability(cls, latency_trend: float, error_rate_trend: float) -> float:
        """
        Estimates failure probability trends.
        """
        prob = 0.05
        if latency_trend > 100.0:
            prob += 0.25
        if error_rate_trend > 0.05:
            prob += 0.45
        return min(prob, 1.0)
