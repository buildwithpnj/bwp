from pydantic import BaseModel
from typing import Optional, List

class AgentRequest(BaseModel):
    session_id: str
    message: str
    user_id: Optional[str] = None

class AgentResponse(BaseModel):
    message: str
    tokens_used: int
    cost_usd: float
    status: str
