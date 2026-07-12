import os
import httpx
import logging
from typing import Dict, Any, Optional
try:
    from .config import AgentConfig
    from .schemas import AgentRequest, AgentResponse
except ImportError:
    from config import AgentConfig
    from schemas import AgentRequest, AgentResponse

logger = logging.getLogger("agent_english_runtime")

async def classify_intent(message: str) -> str:
    """Classifies user intent using a simple keyword routing system (preview safe)."""
    msg = message.lower()
    if any(k in msg for k in ["correct", "grammar", "spell", "check", "fix"]):
        return "english_correction"
    if any(k in msg for k in ["rewrite", "professional", "formal", "rephrase"]):
        return "rewrite"
    if any(k in msg for k in ["hinglish", "meaning", "translate", "hindi"]):
        return "hinglish_to_english"
    if any(k in msg for k in ["explain", "why", "what is", "grammar rule"]):
        return "explanation"
    return "general"

async def run_agent(request: AgentRequest, is_preview: bool = False) -> AgentResponse:
    logger.info(f"AgentEnglish executing session={request.session_id} is_preview={is_preview}")
    
    if is_preview:
        # 1. Classify intent
        intent = await classify_intent(request.message)
        logger.info(f"Preview intent classification: {intent}")
        
        if intent not in AgentConfig.ALLOWED_PREVIEW_INTENTS:
            return AgentResponse(
                message="Out of preview scope. Preview only supports English correction, rewrite, Hinglish translation, or short explanations.",
                tokens_used=0,
                cost_usd=0.0,
                status="blocked"
            )
            
    # Load system prompt
    prompt_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(prompt_dir, "prompts", "coach.txt")
    system_prompt = "You are a professional English coach."
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

    # Call LLM model via httpx (supports OpenAI and Gemini OpenAI-compatible endpoints)
    api_key = AgentConfig.OPENAI_API_KEY
    if not api_key:
        # Fallback Mock response for test/dev modes when API key is missing
        return AgentResponse(
            message=f"[MOCK COACH] I received your request: '{request.message}'. Let's correct that to professional English.",
            tokens_used=120,
            cost_usd=0.0001,
            status="success"
        )

    # Auto-detect Google Gemini API Keys (usually starting with AIza or AQ.)
    is_gemini = api_key.startswith("AIza") or api_key.startswith("AQ.")
    if is_gemini:
        url = "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions"
        model_name = os.environ.get("LLM_MODEL") or "gemini-2.5-flash"
    else:
        url = "https://api.openai.com/v1/chat/completions"
        model_name = AgentConfig.DEFAULT_MODEL
        
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": request.message}
                    ],
                    "max_tokens": AgentConfig.MAX_OUTPUT_LENGTH,
                    "temperature": 0.2
                },
                timeout=12.0
            )
            
            if res.status_code != 200:
                logger.error(f"OpenAI error: {res.status_code} {res.text}")
                return AgentResponse(
                    message="An error occurred while running the coach model.",
                    tokens_used=0,
                    cost_usd=0.0,
                    status="error"
                )
                
            data = res.json()
            message_content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = prompt_tokens + completion_tokens
            
            # Simple Mini pricing calculation
            cost = (prompt_tokens * 0.00000015) + (completion_tokens * 0.00000060)
            
            return AgentResponse(
                message=message_content,
                tokens_used=total_tokens,
                cost_usd=cost,
                status="success"
            )
            
    except Exception as e:
        logger.error(f"Failed to call model: {e}")
        return AgentResponse(
            message="Model pipeline execution failure.",
            tokens_used=0,
            cost_usd=0.0,
            status="error"
        )
