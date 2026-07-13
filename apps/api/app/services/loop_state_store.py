import uuid
from typing import Dict, Any, List

class LoopStateStore:
    _frames: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def initialize_state(cls, prompt: str, tenant_id: str) -> str:
        state_id = str(uuid.uuid4())
        cls._frames[state_id] = {
            "prompt": prompt,
            "tenant_id": tenant_id,
            "steps": [],
            "status": "active"
        }
        return state_id

    @classmethod
    def append_step(cls, state_id: str, step: Dict[str, Any]) -> None:
        if state_id in cls._frames:
            cls._frames[state_id]["steps"].append(step)

    @classmethod
    def get_state(cls, state_id: str) -> Dict[str, Any]:
        return cls._frames.get(state_id) or {}
