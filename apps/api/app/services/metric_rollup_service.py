from typing import List

class MetricRollupService:
    @classmethod
    def calculate_rollup_average(cls, values: List[float]) -> float:
        """
        Returns average metric.
        """
        if not values:
            return 0.0
        return sum(values) / len(values)
