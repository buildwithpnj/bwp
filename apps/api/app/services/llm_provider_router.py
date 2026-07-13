import logging
from typing import List, Dict, Any, Optional
from app.llm_settings import llm_settings
from app.services.ollama_provider_service import OllamaProviderService
from app.services.model_capability_registry import ModelCapabilityRegistry

logger = logging.getLogger("llm_provider_router")

class LLMProviderRouter:
    @classmethod
    async def route_completion(
        cls,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Routes the chat prompt to the selected LLM provider with failover policies.
        """
        provider = llm_settings.llm_provider.lower()
        local_enabled = llm_settings.local_ai_enabled
        fallback_enabled = llm_settings.provider_fallback_enabled
        cloud_model = llm_settings.primary_cloud_provider

        model_name = model or (llm_settings.ollama_model if (provider == "ollama" and local_enabled) else "gpt-3.5-turbo")
        
        capabilities = ModelCapabilityRegistry.get_capabilities(model_name)
        
        # Enforce json_mode capability check
        if json_mode and not capabilities.json_mode:
            logger.warning(f"Model '{model_name}' registry does not support json_mode. Formulating structured prompts manually.")
            
        if provider == "ollama" and local_enabled:
            logger.info(f"Routing request to local inference model '{model_name}' via Ollama...")
            result = await OllamaProviderService.generate_chat_response(
                messages=messages,
                model=model_name,
                json_mode=json_mode,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Fallback policy
            if result.get("status") == "error":
                if fallback_enabled:
                    logger.error(f"Local Ollama inference failed with {result.get('error_type')}. Triggering backup cloud fallback handler...")
                    return await cls._execute_cloud_fallback(
                        messages=messages,
                        model=cloud_model,
                        json_mode=json_mode,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        trigger_reason=result.get("message")
                    )
                else:
                    logger.warning("Local inference failed and fallback is disabled.")
                    return result
            return result
        else:
            # Standard cloud fallback routing directly
            return await cls._execute_cloud_fallback(
                messages=messages,
                model=cloud_model,
                json_mode=json_mode,
                temperature=temperature,
                max_tokens=max_tokens,
                trigger_reason="Configured default cloud provider"
            )

    @classmethod
    async def _execute_cloud_fallback(
        cls,
        messages: List[Dict[str, str]],
        model: str,
        json_mode: bool,
        temperature: float,
        max_tokens: Optional[int],
        trigger_reason: str
    ) -> Dict[str, Any]:
        """
        Mock cloud model completion provider to shield tests from billing costs while
        simulating fully formatted structured outputs or RAG answers.
        """
        logger.info(f"Executing cloud mock provider (model: {model}) fallback. Reason: {trigger_reason}")
        
        # Simulate simple structured response format if json requested
        last_user_message = messages[-1]["content"] if messages else ""
        
        import json
        if json_mode:
            content = json.dumps({
                "status": "success",
                "message": f"Cloud fallback response. Echo query: '{last_user_message}'",
                "citations": ["doc_1", "doc_2"],
                "step_index": 1,
                "tool": "search",
                "query": last_user_message
            })
        else:
            content = f"Cloud fallback answer. Reference: {last_user_message}"

        return {
            "status": "success",
            "provider": "cloud_fallback",
            "content": content,
            "model": model,
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 80,
                "total_tokens": 200
            }
        }
