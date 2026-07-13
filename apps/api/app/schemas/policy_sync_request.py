from pydantic import BaseModel, Field
from typing import List

class PolicySyncRequest(BaseModel):
    source_env: str = Field(..., description="E.g. staging")
    target_env: str = Field(..., description="E.g. production")
    target_nodes: List[str] = Field(default_factory=list)
    target_tenants: List[str] = Field(default_factory=list)
    signature: str = Field(..., description="Admin cryptographic signature")
