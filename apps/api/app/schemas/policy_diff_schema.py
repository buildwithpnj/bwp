from pydantic import BaseModel, Field
from typing import Dict, Any

class PolicyDiffSchema(BaseModel):
    changed_keys: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="E.g. {'modality_limit': {'old': '25MB', 'new': '50MB'}}")
    severity: str = "low"
