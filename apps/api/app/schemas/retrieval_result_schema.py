from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ChunkResultSchema(BaseModel):
    chunk_id: str
    document_id: str
    chunk_text: str
    chunk_summary: str
    confidence_score: float

class RetrievalResultSchema(BaseModel):
    trace_id: str
    query_text: str
    strategy_used: str
    confidence_score: float
    latency_ms: float
    chunks: List[ChunkResultSchema] = Field(default_factory=list)
