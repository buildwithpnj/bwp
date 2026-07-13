from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.keyword_index_service import KeywordIndexService
from app.services.embedding_retrieval_service import EmbeddingRetrievalService
from app.services.retrieval_candidate_merger import RetrievalCandidateMerger
from app.services.reranking_service import RerankingService
from app.services.tenant_retrieval_guard import TenantRetrievalGuard

class HybridRetrievalService:
    @classmethod
    async def retrieve(
        cls,
        db: AsyncSession,
        tenant_id: str,
        query: str,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching chunks via combination of keyword matching and vector similarity.
        """
        # Strict tenant partitioning check
        TenantRetrievalGuard.validate_tenant(tenant_id)
        
        # Fetch chunks from DB
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.tenant_id == tenant_id)
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
        
        # 1. Lexical filtering
        keywords = KeywordIndexService.extract_keywords(query)
        lexical_candidates = []
        for cand in candidates:
            cand_words = KeywordIndexService.extract_keywords(cand["chunk_text"])
            if keywords.intersection(cand_words):
                lexical_candidates.append(cand)
                
        # 2. Vector similarity search
        vector_candidates = EmbeddingRetrievalService.fetch_similar_chunks(query, candidates)
        
        # 3. Deterministic candidate merging & deduplication
        merged = RetrievalCandidateMerger.merge_candidates(lexical_candidates, vector_candidates)
        
        # 4. Rerank final matches
        reranked = RerankingService.reorder_candidates(query, merged)
        return reranked
