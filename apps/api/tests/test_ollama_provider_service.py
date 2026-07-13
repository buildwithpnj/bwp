import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ollama_provider_service import OllamaProviderService
from app.llm_settings import llm_settings

@pytest.mark.asyncio
async def test_ollama_completion_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value={
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "Hello local developer!"
        },
        "prompt_eval_count": 10,
        "eval_count": 15,
        "done": True
    })

    # Mock the AsyncClient.post method
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        result = await OllamaProviderService.generate_chat_response(
            messages=[{"role": "user", "content": "hi"}],
            model="llama3"
        )
        
        assert result["status"] == "success"
        assert result["content"] == "Hello local developer!"
        assert result["usage"]["prompt_tokens"] == 10
        assert result["usage"]["completion_tokens"] == 15
        assert result["usage"]["total_tokens"] == 25

@pytest.mark.asyncio
async def test_ollama_connection_failure():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.ConnectError("Connection refused")
        
        result = await OllamaProviderService.generate_chat_response(
            messages=[{"role": "user", "content": "hi"}],
            model="llama3"
        )
        
        assert result["status"] == "error"
        assert result["error_type"] == "connection_failure"
        assert "Ollama endpoint offline" in result["message"]

@pytest.mark.asyncio
async def test_ollama_timeout_failure():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.TimeoutException("Request timed out")
        
        result = await OllamaProviderService.generate_chat_response(
            messages=[{"role": "user", "content": "hi"}],
            model="llama3"
        )
        
        assert result["status"] == "error"
        assert result["error_type"] == "timeout_failure"
        assert "timed out" in result["message"]
