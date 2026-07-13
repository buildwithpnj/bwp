class PreventiveRecommendationService:
    @classmethod
    def generate_recommendation(cls, risk_score: float) -> str:
        """
        Suggests preventive actions.
        """
        if risk_score > 0.6:
            return "recommend_degraded_fallback_mode"
        return "continue_normal_monitoring"
