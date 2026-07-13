class RiskThresholdPolicyService:
    @classmethod
    def check_threshold_breach(cls, risk_score: float) -> bool:
        """
        Triggers safety gates if risk score > 0.8.
        """
        return risk_score > 0.8
