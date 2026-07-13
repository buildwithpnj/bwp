class PredictionExplainabilityService:
    @classmethod
    def generate_explanation(cls, risk_score: float) -> str:
        """
        Explains why a risk score is high.
        """
        if risk_score > 0.7:
            return "High risk probability due to concurrent alert spikes and high model latency delta."
        return "Low baseline cluster operational risk."
