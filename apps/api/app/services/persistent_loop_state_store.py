import uuid
from typing import Dict, Any, List, Optional

class PersistentLoopStateStore:
    # Memory-based static dict simulating persistent database storage
    _db_store: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def save_state(
        cls,
        state_id: str,
        prompt: str,
        tenant_id: str,
        steps: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]],
        status: str = "active",
        stop_reason: Optional[str] = None
    ) -> None:
        """
        Saves loop state.
        """
        cls._db_store[state_id] = {
            "state_id": state_id,
            "prompt": prompt,
            "tenant_id": tenant_id,
            "steps": steps,
            "evidence": evidence,
            "status": status,
            "stop_reason": stop_reason
        }

    @classmethod
    def get_state(cls, state_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves state record from database storage.
        """
        return cls._db_store.get(state_id)

    @classmethod
    def list_all_traces(cls) -> List[Dict[str, Any]]:
        return list(cls._db_store.values())
