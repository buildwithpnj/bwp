import time
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.schemas.retrieval_request_schema import RetrievalRequestSchema
from app.schemas.retrieval_result_schema import RetrievalResultSchema, ChunkResultSchema
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.query_rewrite_service import QueryRewriteService
from app.services.reranking_service import RerankingService
from app.services.retrieval_observability_service import RetrievalObservabilityService
from app.services.retrieval_feedback_service import RetrievalFeedbackService

router = APIRouter(prefix="/api/retrieval", tags=["Hybrid RAG Retrieval Layer"])

@router.post("/query", response_model=RetrievalResultSchema, status_code=status.HTTP_200_OK)
async def query_knowledge_base(
    req: RetrievalRequestSchema,
    current_user: CurrentUser,
    db: DB
):
    """
    Executes hybrid (keyword + vector mock) retrieval matching flows.
    """
    start_time = time.time()
    
    # 1. Rewrite if sync abbreviations exists
    rewritten = QueryRewriteService.expand_query(req.query)
    
    # 2. Fetch candidates from DB
    stmt = select(KnowledgeChunk).where(KnowledgeChunk.tenant_id == req.tenant_id)
    res = await db.execute(stmt)
    chunks = res.scalars().all()
    
    candidates = [
        {
            "chunk_id": c.id,
            "document_id": c.document_id,
            "chunk_text": c.chunk_text,
            "chunk_summary": c.chunk_summary
        }
        for c in chunks
    ]
    
    # 3. Rerank
    reranked = RerankingService.reorder_candidates(rewritten, candidates)
    
    latency = (time.time() - start_time) * 1000.0
    confidence = 0.95 if reranked else 0.1
    
    # 4. Log trace
    trace = await RetrievalObservabilityService.log_trace(
        db, req.query, rewritten, "hybrid_keyword_vector", latency, confidence
    )
    
    return RetrievalResultSchema(
        trace_id=trace.id,
        query_text=req.query,
        strategy_used="hybrid_keyword_vector",
        confidence_score=confidence,
        latency_ms=latency,
        chunks=[
            ChunkResultSchema(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                chunk_text=r["chunk_text"],
                chunk_summary=r["chunk_summary"],
                confidence_score=r["confidence_score"]
            )
            for r in reranked[:3]
        ]
    )

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    trace_id: str,
    score: int,
    notes: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Accepts user evaluations parameters to record tuning scores.
    """
    fb = await RetrievalFeedbackService.record_feedback(db, trace_id, score, notes)
    return {"feedback_id": fb.id, "status": "recorded"}
