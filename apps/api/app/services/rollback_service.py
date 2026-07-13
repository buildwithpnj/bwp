from typing import Dict, Any

class RollbackService:
    _rollbacks_executed = []

    @classmethod
    def trigger_rollback(cls, action_name: str, payload: Dict[str, Any], tenant_id: str) -> None:
        """
        Executes compensation operations to reverse write outcomes.
        """
        cls._rollbacks_executed.append({
            "action": action_name,
            "payload": payload,
            "tenant_id": tenant_id
        })
