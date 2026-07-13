import logging
from typing import List
from app.models.action_models import ActionLog

logger = logging.getLogger("failure_pattern_service")

class FailurePatternService:
    @classmethod
    def analyze_patterns(cls, log: ActionLog) -> List[str]:
        """
        Analyzes a single ActionLog for common execution failure signatures.
        """
        patterns = []
        
        # 1. Retry thresholds check
        if log.retry_count is not None and log.retry_count >= 2:
            patterns.append("repeated_retry_pattern")
            
        # 2. Timeout detections
        err_msg = (log.error_message or "").lower()
        last_err = (log.last_error or "").lower()
        if "timeout" in err_msg or "timeout" in last_err:
            patterns.append("timeout_pattern")
            
        # 3. Duplicate blocking checks
        if "duplicate" in err_msg or "duplicate" in last_err or "idempotency" in last_err:
            patterns.append("duplicate_block_pattern")
            
        return patterns
