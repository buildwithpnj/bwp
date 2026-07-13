import httpx
import logging
from typing import List, Dict, Any, Optional
from app.llm_settings import llm_settings

logger = logging.getLogger("ollama_provider")

class OllamaProviderService:
    @classmethod
    async def generate_chat_response(
        cls,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calls local Ollama inference server for chat completions.
        """
        model_name = model or llm_settings.ollama_model
        base_url = llm_settings.ollama_base_url.rstrip("/")
        url = f"{base_url}/api/chat"

        payload = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        if json_mode:
            payload["format"] = "json"

        timeout = httpx.Timeout(float(llm_settings.ollama_timeout_seconds), connect=5.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                res_data = response.json()
                
                content = res_data.get("message", {}).get("content", "")
                
                # Mock token calculation or parse token indicators from Ollama response meta info if available
                prompt_eval_count = res_data.get("prompt_eval_count", 0)
                eval_count = res_data.get("eval_count", 0)
                total_tokens = prompt_eval_count + eval_count

                return {
                    "status": "success",
                    "content": content,
                    "model": model_name,
                    "usage": {
                        "prompt_tokens": prompt_eval_count,
                        "completion_tokens": eval_count,
                        "total_tokens": total_tokens
                    }
                }
            except httpx.ConnectError as e:
                logger.error(f"Failed to connect to local Ollama inference server at {url}: {e}")
                return {
                    "status": "error",
                    "error_type": "connection_failure",
                    "message": f"Ollama endpoint offline. Verify 'ollama serve' is running. Detail: {e}"
                }
            except httpx.TimeoutException as e:
                logger.error(f"Timeout calling local Ollama model {model_name} at {url}: {e}")
                return {
                    "status": "error",
                    "error_type": "timeout_failure",
                    "message": f"Ollama inference timed out after {llm_settings.ollama_timeout_seconds} seconds."
                }
            except Exception as e:
                logger.error(f"Unexpected error calling local Ollama client: {e}")
                return {
                    "status": "error",
                    "error_type": "unexpected_failure",
                    "message": str(e)
                }
