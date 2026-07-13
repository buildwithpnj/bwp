import uuid
from typing import Dict, Any

class ActionAuditLogService:
    _logs = {}

    @classmethod
    def log_execution(cls, action_name: str, payload: Dict[str, Any], tenant_id: str) -> str:
        log_id = str(uuid.uuid4())
        cls._logs[log_id] = {
            "id": log_id,
            "action": action_name,
            "payload": payload,
            "tenant_id": tenant_id,
            "status": "logged"
        }
        return log_id
