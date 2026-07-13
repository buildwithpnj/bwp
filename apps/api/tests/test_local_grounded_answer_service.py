import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.local_grounded_answer_service import LocalGroundedAnswerService
from app.llm_settings import llm_settings

@pytest.mark.asyncio
async def test_generate_grounded_answer_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value={
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "This is a grounded answer for git sync configuration rules."
        },
        "prompt_eval_count": 5,
        "eval_count": 10,
        "done": True
    })
    
    compressed_pack = {
        "evidence_blocks": [
            {"chunk_id": "c1", "summary": "git sync configuration rules"}
        ]
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        llm_settings.llm_provider = "ollama"
        
        result = await LocalGroundedAnswerService.generate_grounded_answer(
            query="how to sync",
            compressed_pack=compressed_pack,
            confidence_score=0.8
        )
        
        assert result["grounded"] is True
        assert "git sync" in result["answer"]
        assert len(result["citations"]) == 1

@pytest.mark.asyncio
async def test_generate_grounded_answer_abstain_low_confidence():
    compressed_pack = {
        "evidence_blocks": [
            {"chunk_id": "c1", "summary": "git sync configuration rules"}
        ]
    }
    
    result = await LocalGroundedAnswerService.generate_grounded_answer(
        query="how to sync",
        compressed_pack=compressed_pack,
        confidence_score=0.4 # Under 0.6 threshold
    )
    
    assert result["grounded"] is False
    assert "cannot answer this question with sufficient confidence" in result["answer"]
    assert len(result["citations"]) == 0

@pytest.mark.asyncio
async def test_generate_grounded_answer_abstain_no_citations():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value={
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "I have absolutely no idea how to do that operation."
        },
        "prompt_eval_count": 5,
        "eval_count": 10,
        "done": True
    })
    
    compressed_pack = {
        "evidence_blocks": [
            {"chunk_id": "c1", "summary": "cryptographic OAuth token exchange database model"}
        ]
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        llm_settings.llm_provider = "ollama"
        
        result = await LocalGroundedAnswerService.generate_grounded_answer(
            query="how to auth",
            compressed_pack=compressed_pack,
            confidence_score=0.8
        )
        
        assert result["grounded"] is False
        assert "Abstaining from answering" in result["answer"]
        assert len(result["citations"]) == 0
