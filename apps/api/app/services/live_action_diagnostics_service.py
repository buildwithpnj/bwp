import httpx
import logging
from typing import Dict, Any
from app.llm_settings import llm_settings

logger = logging.getLogger("live_action_diagnostics")

class LiveActionDiagnosticsService:
    @classmethod
    async def run_diagnostics(cls) -> Dict[str, Any]:
        """
        Runs connection check to local/remote Ollama instance and returns metrics.
        """
        base_url = llm_settings.ollama_base_url.rstrip("/")
        url = f"{base_url}/api/tags"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url, headers={"ngrok-skip-browser-warning": "1"})
                if res.status_code == 200:
                    return {
                        "status": "healthy",
                        "message": "Connection to local Ollama instance is healthy.",
                        "tags": res.json().get("models", [])
                    }
                else:
                    return {
                        "status": "degraded",
                        "message": f"Server responded with status code {res.status_code}.",
                        "tags": []
                    }
        except Exception as e:
            logger.error(f"Live action diagnostics failed: {e}")
            return {
                "status": "offline",
                "message": f"Connection failed: {str(e)}",
                "tags": []
            }
