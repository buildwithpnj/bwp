from pydantic import BaseModel, Field

class PredictionExplanationSchema(BaseModel):
    risk_snapshot_id: str = Field(..., max_length=36)
    explanation: str = Field(..., max_length=1000)
