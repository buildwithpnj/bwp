from pydantic import BaseModel, Field
from typing import Optional

class KnowledgeDocumentCreate(BaseModel):
    tenant_id: str = Field(..., max_length=36)
    source_type: str = Field(..., max_length=50)
    source_path: str = Field(..., max_length=255)
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)
    content_hash: str = Field(..., max_length=64)
    canonical_text: str = Field(...)
    visibility_scope: str = Field("internal", max_length=20)
