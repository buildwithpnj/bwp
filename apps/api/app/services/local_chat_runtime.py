from typing import List, Dict, Any, Optional
from app.services.llm_provider_router import LLMProviderRouter

class LocalChatRuntime:
    @classmethod
    async def chat(
        cls,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Executes a simple local inference chat message with context history.
        """
        chat_messages = []
        if history:
            chat_messages.extend(history)
            
        chat_messages.append({"role": "user", "content": user_message})
        
        response = await LLMProviderRouter.route_completion(
            messages=chat_messages,
            json_mode=False
        )
        
        return response
