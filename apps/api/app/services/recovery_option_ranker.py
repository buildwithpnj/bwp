from typing import List
from app.schemas.recovery_plan import RecoveryOption

class RecoveryOptionRanker:
    @classmethod
    def rank_options(cls, options: List[RecoveryOption]) -> List[RecoveryOption]:
        """
        Sorts recovery options by risk score ascending (safest option first).
        """
        return sorted(options, key=lambda opt: opt.risk_score)
