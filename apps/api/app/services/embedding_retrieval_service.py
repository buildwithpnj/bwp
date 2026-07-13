from typing import List, Dict, Any
from app.services.embedding_index_service import EmbeddingIndexService
from app.services.vector_store_service import VectorStoreService

class EmbeddingRetrievalService:
    @classmethod
    def fetch_similar_chunks(
        cls,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Coordinates embedding lookup and vector similarity filters.
        """
        query_vector = EmbeddingIndexService.generate_mock_embedding(query)
        # inject fake mock vectors to candidates for cosine calculations
        for cand in candidates:
            cand["vector"] = EmbeddingIndexService.generate_mock_embedding(cand["chunk_text"])
            
        results = VectorStoreService.search_similar_vectors(query_vector, candidates, top_k)
        return [
            {
                "chunk_id": r["chunk"]["chunk_id"],
                "document_id": r["chunk"]["document_id"],
                "chunk_text": r["chunk"]["chunk_text"],
                "chunk_summary": r["chunk"]["chunk_summary"],
                "score": r["score"]
            }
            for r in results
        ]
