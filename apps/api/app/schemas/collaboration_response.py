from pydantic import BaseModel
from typing import Dict, Any, List

class CollaborationResponse(BaseModel):
    collaboration_id: str
    coordination_status: str  # merged, failed
    final_merged_result: Dict[str, Any]
    handoffs_count: int
    used_tokens: float
