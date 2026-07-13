from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SimulationRequest(BaseModel):
    workflow_run_id: str
    plan_steps: List[Dict[str, Any]] = Field(..., min_items=1)
