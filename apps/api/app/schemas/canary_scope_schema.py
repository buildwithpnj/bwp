from pydantic import BaseModel, Field
from typing import List

class CanaryScopeSchema(BaseModel):
    tenant_ids: List[str] = Field(default_factory=list)
    node_ips: List[str] = Field(default_factory=list)
