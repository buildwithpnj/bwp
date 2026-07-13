class WorkflowEvalService:
    @classmethod
    def evaluate_success_probability(cls, success_score: float) -> str:
        """
        Translates success floats into explainable category ratings.
        """
        if success_score >= 0.8:
            return "high"
        if success_score >= 0.5:
            return "moderate"
        return "low"
