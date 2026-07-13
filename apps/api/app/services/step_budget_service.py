import time

class StepBudgetService:
    def __init__(
        self,
        max_steps: int = 5,
        max_retries: int = 3,
        max_tokens: int = 4000,
        time_limit_sec: float = 120.0
    ):
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.max_tokens = max_tokens
        self.time_limit_sec = time_limit_sec
        
        self.steps_taken = 0
        self.retries_taken = 0
        self.tokens_consumed = 0
        self.start_time = time.perf_counter()

    def consume_step(self) -> None:
        self.steps_taken += 1

    def consume_retry(self) -> None:
        self.retries_taken += 1

    def consume_tokens(self, count: int) -> None:
        self.tokens_consumed += count

    def get_elapsed_time(self) -> float:
        return time.perf_counter() - self.start_time

    def has_budget(self) -> bool:
        """
        Returns true if the loop is within step, retry, token, and time limits.
        """
        if self.steps_taken >= self.max_steps:
            return False
        if self.retries_taken >= self.max_retries:
            return False
        if self.tokens_consumed >= self.max_tokens:
            return False
        if self.get_elapsed_time() >= self.time_limit_sec:
            return False
        return True
