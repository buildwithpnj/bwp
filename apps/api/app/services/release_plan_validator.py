class ReleasePlanValidator:
    @classmethod
    def validate_plan_readiness(cls, scope: str, percentage: int) -> bool:
        """
        Validates target parameters configuration bounds.
        """
        if percentage < 0 or percentage > 100:
            return False
        if not scope:
            return False
        return True
