class PolicyChangeGuard:
    @classmethod
    def validate_policy_shift(cls, current_val: float, proposed_val: float) -> bool:
        """
        Guards against excessive policy threshold changes to prevent wild swings.
        """
        shift = abs(current_val - proposed_val)
        return shift <= 0.5
