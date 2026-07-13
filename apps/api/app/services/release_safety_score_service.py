class ReleaseSafetyScoreService:
    @classmethod
    def calculate_safety_score(cls, has_drift: bool, failure_delta: float) -> float:
        """
        Estimates the deployment risk score.
        """
        score = 1.0
        if has_drift:
            score -= 0.3
        if failure_delta > 0.1:
            score -= 0.4
        return max(score, 0.0)
