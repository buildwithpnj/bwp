import httpx
import logging
from typing import Dict, Any
from app.llm_settings import llm_settings

logger = logging.getLogger("local_model_health")

class LocalModelHealthService:
    @classmethod
    async def check_health(cls) -> Dict[str, Any]:
        """
        Polls the local Ollama inference service status and returns health states.
        """
        base_url = llm_settings.ollama_base_url.rstrip("/")
        url = f"{base_url}/"

        timeout = httpx.Timeout(3.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "provider": "ollama",
                        "base_url": llm_settings.ollama_base_url,
                        "model": llm_settings.ollama_model,
                        "details": "Local Ollama server is online and responding."
                    }
                else:
                    return {
                        "status": "degraded",
                        "provider": "ollama",
                        "base_url": llm_settings.ollama_base_url,
                        "model": llm_settings.ollama_model,
                        "details": f"Server returned status code {response.status_code}."
                    }
            except Exception as e:
                logger.error(f"Local Ollama health check failed: {e}")
                return {
                    "status": "offline",
                    "provider": "ollama",
                    "base_url": llm_settings.ollama_base_url,
                    "model": llm_settings.ollama_model,
                    "details": f"Cannot connect to local server. Detail: {e}"
                }
