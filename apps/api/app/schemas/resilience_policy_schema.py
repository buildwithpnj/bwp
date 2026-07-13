from pydantic import BaseModel, Field

class ResiliencePolicyCreate(BaseModel):
    trigger_type: str = Field(..., max_length=50)
    affected_scope: str = Field(..., max_length=100)
    degradation_level: str = Field("degraded", max_length=20)
    token_budget_reduction_factor: float = Field(0.5, ge=0.0, le=1.0)
