from pydantic import BaseModel, Field

class AnomalySignalSchema(BaseModel):
    tenant_id: str = Field(..., max_length=36)
    signal_type: str = Field(..., max_length=50)
    severity: str = Field("medium", max_length=20)
    summary: str = Field(..., max_length=500)
