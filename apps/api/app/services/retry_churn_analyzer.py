class RetryChurnAnalyzer:
    _reflection_triggers: int = 0
    _no_progress_halts: int = 0

    @classmethod
    def record_reflection_trigger(cls) -> None:
        cls._reflection_triggers += 1

    @classmethod
    def record_no_progress_halt(cls) -> None:
        cls._no_progress_halts += 1

    @classmethod
    def get_retry_churn_stats(cls) -> dict:
        return {
            "reflection_triggers_count": cls._reflection_triggers,
            "no_progress_halts_count": cls._no_progress_halts
        }
        
    @classmethod
    def clear_churn_stats(cls) -> None:
        cls._reflection_triggers = 0
        cls._no_progress_halts = 0
