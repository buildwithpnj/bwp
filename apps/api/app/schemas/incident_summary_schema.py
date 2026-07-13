from pydantic import BaseModel, Field

class IncidentSummarySchema(BaseModel):
    incident_id: str = Field(..., max_length=36)
    status: str = Field(..., max_length=20)
    summary: str = Field(..., max_length=500)
