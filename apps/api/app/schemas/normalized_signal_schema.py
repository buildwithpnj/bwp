from pydantic import BaseModel, Field
from typing import List, Dict, Any

class NormalizedSignal(BaseModel):
    media_type: str
    extracted_text: str
    detected_entities: Dict[str, Any] = Field(default_factory=dict)
    intent_hints: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    safety_flags: Dict[str, bool] = Field(default_factory=dict)
    suggested_workflow_type: str = "generic_action"
