from pydantic import BaseModel
from typing import List, Dict, Any

class SimulationResult(BaseModel):
    predicted_success_score: float
    likely_failures: List[str]
    risk_score: float
    simulated_outcome_summary: str
