from pydantic import BaseModel, Field

class TelemetryEventCreate(BaseModel):
    tenant_id: str = Field(..., max_length=36)
    node_id: str = Field(..., max_length=50)
    service_name: str = Field(..., max_length=50)
    environment: str = Field(..., max_length=50)
    signal_type: str = Field(..., max_length=20)  # log, metric, event
    payload: str = Field(..., max_length=1000)
