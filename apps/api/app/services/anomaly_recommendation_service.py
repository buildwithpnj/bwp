class AnomalyRecommendationService:
    @classmethod
    def get_recommendations(cls, signal_type: str) -> list:
        """
        Emits structured prevention triggers based on signal criteria.
        """
        if signal_type == "quota_breach":
            return ["increase_limit", "throttle_noncritical_runs"]
        return ["verify_node_network", "review_last_governance_sync"]
