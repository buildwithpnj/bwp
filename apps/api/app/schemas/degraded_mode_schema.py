from pydantic import BaseModel, Field

class DegradedModeSchema(BaseModel):
    affected_scope: str = Field(..., max_length=100)
    activated_features: str = Field(..., max_length=500)
    disabled_features: str = Field(..., max_length=500)
