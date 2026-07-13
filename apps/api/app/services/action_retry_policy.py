class ActionRetryPolicy:
    # Action name mapping to allowed max retries
    RETRYABLE_ACTIONS = {
        "create_followup_practice": 3,
        "create_lesson_note": 2
    }

    @classmethod
    def should_retry(cls, action_name: str, current_retry_count: int) -> bool:
        """Determines if the action qualifies for automatic retry based on constraints."""
        max_allowed = cls.RETRYABLE_ACTIONS.get(action_name, 0)
        current = current_retry_count if current_retry_count is not None else 0
        return current < max_allowed
