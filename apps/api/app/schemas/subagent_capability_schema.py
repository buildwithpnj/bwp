from pydantic import BaseModel
from typing import List

class SubAgentCapability(BaseModel):
    specialist_type: str
    purpose: str
    allowed_input_domains: List[str]
    max_delegation_steps: int
    allowed_tools: List[str]
    risk_level: str
    token_budget_cap: float
    timeout_ms: int
