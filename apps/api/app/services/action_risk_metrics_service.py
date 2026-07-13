class ActionRiskMetricsService:
    _blocked_actions_count: int = 0
    _idempotent_skips_count: int = 0

    @classmethod
    def record_blocked_action(cls) -> None:
        cls._blocked_actions_count += 1

    @classmethod
    def record_idempotent_skip(cls) -> None:
        cls._idempotent_skips_count += 1

    @classmethod
    def get_risk_metrics(cls) -> dict:
        return {
            "blocked_actions_count": cls._blocked_actions_count,
            "idempotent_skips_count": cls._idempotent_skips_count
        }

    @classmethod
    def clear_risk_metrics(cls) -> None:
        cls._blocked_actions_count = 0
        cls._idempotent_skips_count = 0
