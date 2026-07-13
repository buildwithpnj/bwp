import logging
from typing import List, Dict, Any, Optional
from app.services.llm_provider_router import LLMProviderRouter
from app.services.structured_output_repair_service import StructuredOutputRepairService

logger = logging.getLogger("provider_fallback")

class ProviderFallbackService:
    @classmethod
    async def execute_with_fallback(
        cls,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes completion against selected provider, falls back to cloud mock on failure,
        and logs error details.
        """
        # Try active provider (which might be Ollama)
        result = await LLMProviderRouter.route_completion(
            messages=messages,
            json_mode=json_mode,
            model=model
        )

        if result.get("status") == "success":
            # If JSON mode requested, verify it is parseable
            if json_mode:
                content = result.get("content", "")
                parsed = StructuredOutputRepairService.parse_repaired_json(content)
                if parsed is None:
                    logger.error("JSON payload is unparseable even after repair. Executing cloud fallback...")
                    # Failover to cloud
                    return await LLMProviderRouter._execute_cloud_fallback(
                        messages=messages,
                        model="gpt-3.5-turbo",
                        json_mode=json_mode,
                        temperature=0.2,
                        max_tokens=None,
                        trigger_reason="Malformed JSON output from primary local provider"
                    )
            return result
        else:
            # Fallback already handled by router, return result
            return result
