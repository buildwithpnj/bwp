from pydantic import BaseModel, Field
from typing import Optional

class KnowledgeChunkCreate(BaseModel):
    document_id: str = Field(..., max_length=36)
    tenant_id: str = Field(..., max_length=36)
    chunk_text: str = Field(...)
    chunk_summary: str = Field(...)
    token_count: int = Field(..., ge=0)
    heading_hierarchy: Optional[str] = Field(None, max_length=255)
