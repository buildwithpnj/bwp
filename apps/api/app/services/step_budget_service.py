class StepBudgetService:
    def __init__(self, max_steps: int = 5):
        self.max_steps = max_steps
        self.steps_taken = 0

    def consume_step(self) -> None:
        self.steps_taken += 1

    def has_budget(self) -> bool:
        return self.steps_taken < self.max_steps
