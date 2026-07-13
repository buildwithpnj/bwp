from pydantic import BaseModel, Field

class RolloutDecisionSchema(BaseModel):
    rollout_id: str = Field(..., max_length=36)
    decision: str = Field(..., description="E.g. expand, pause, resume, rollback")
    reason: str = Field(..., max_length=255)
