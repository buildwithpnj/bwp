from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class RetrievalRequestSchema(BaseModel):
    query: str = Field(...)
    tenant_id: str = Field(..., max_length=36)
    page_scope: Optional[str] = Field(None, max_length=50)
    filters: Optional[Dict[str, Any]] = Field(None)
