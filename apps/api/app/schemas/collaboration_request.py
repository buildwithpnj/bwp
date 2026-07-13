from pydantic import BaseModel, Field
from typing import List, Dict, Any

class CollaborationRequest(BaseModel):
    workflow_run_id: str
    participating_agents: List[str]
    coordination_goals: Dict[str, str] = Field(default_factory=dict)
    max_steps: int = 10
