from pydantic import BaseModel, Field

class OpsRiskCreate(BaseModel):
    tenant_scope: str = Field(..., max_length=36)
    cluster_scope: str = Field(..., max_length=100)
    risk_score: float = Field(0.0, ge=0.0, le=1.0)
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)
    recommended_prevention: str = Field(..., max_length=500)
