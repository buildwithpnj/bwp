import pytest
from app.services.rag_answer_service import RAGAnswerService
from app.services.page_aware_retrieval_service import PageAwareRetrievalService

def test_rag_generation_rules():
    # 1. Page Context narrow
    q = PageAwareRetrievalService.inject_page_context("settings", "active tokens")
    assert q == "[settings] active tokens"
    
    # 2. Cautious fallback response if confidence score is low
    low_conf = RAGAnswerService.generate_answer("query", {}, confidence_score=0.4)
    assert "cannot answer" in low_conf["answer"]
    
    # 3. Grounded generation if confidence is strong
    pack = {
        "query": "active tokens",
        "evidence_blocks": [
            {"chunk_id": "c1", "text": "This is settings config content", "summary": "settings config"}
        ]
    }
    strong_conf = RAGAnswerService.generate_answer("active tokens", pack, confidence_score=0.9)
    assert strong_conf["grounded"] is True
    assert len(strong_conf["citations"]) > 0
