class AnomalySeverityService:
    @classmethod
    def evaluate_severity(cls, error_count: int) -> str:
        """
        Rates signal levels based on threshold values.
        """
        if error_count > 10:
            return "critical"
        elif error_count > 3:
            return "high"
        return "medium"
