import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("action_observability")

class ActionObservabilityService:
    @classmethod
    def log_event(
        cls, 
        event_name: str, 
        user_id: str, 
        action_name: str, 
        action_log_id: str, 
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """Logs a structured JSON line event to standard observability logs."""
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_name,
            "user_id": user_id,
            "action_name": action_name,
            "action_log_id": action_log_id,
        }
        if extra:
            payload.update(extra)
            
        # Emit as machine-readable structured logs
        logger.info(json.dumps(payload))
        
        # Also feed the local metrics service aggregates
        try:
            from app.services.action_metrics_service import ActionMetricsService
            ActionMetricsService.record_event(event_name, user_id, action_name, extra)
        except Exception:
            pass  # Avoid circular dependency or metric logging failures breaking execution
