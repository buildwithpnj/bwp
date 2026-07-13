from typing import Dict, Any

class ModelCapabilities:
    def __init__(
        self,
        chat: bool = True,
        json_mode: bool = False,
        tool_use: bool = False,
        long_context: bool = False,
        reasoning_stability: str = "medium"
    ):
        self.chat = chat
        self.json_mode = json_mode
        self.tool_use = tool_use
        self.long_context = long_context
        self.reasoning_stability = reasoning_stability

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chat": self.chat,
            "json_mode": self.json_mode,
            "tool_use": self.tool_use,
            "long_context": self.long_context,
            "reasoning_stability": self.reasoning_stability
        }

class ModelCapabilityRegistry:
    # Pre-configured model capability profiles
    _registry: Dict[str, ModelCapabilities] = {
        "gpt-4o": ModelCapabilities(chat=True, json_mode=True, tool_use=True, long_context=True, reasoning_stability="high"),
        "gpt-3.5-turbo": ModelCapabilities(chat=True, json_mode=True, tool_use=True, long_context=False, reasoning_stability="high"),
        "gemini-2.0-flash": ModelCapabilities(chat=True, json_mode=True, tool_use=True, long_context=True, reasoning_stability="high"),
        "claude-3-5-sonnet": ModelCapabilities(chat=True, json_mode=True, tool_use=True, long_context=True, reasoning_stability="high"),
        # Local inference models via Ollama
        "llama3": ModelCapabilities(chat=True, json_mode=True, tool_use=False, long_context=False, reasoning_stability="medium"),
        "qwen2.5": ModelCapabilities(chat=True, json_mode=True, tool_use=True, long_context=True, reasoning_stability="high"),
        "mistral": ModelCapabilities(chat=True, json_mode=False, tool_use=False, long_context=False, reasoning_stability="medium"),
        "phi3": ModelCapabilities(chat=True, json_mode=False, tool_use=False, long_context=False, reasoning_stability="low"),
    }

    @classmethod
    def get_capabilities(cls, model_name: str) -> ModelCapabilities:
        """
        Returns model capabilities profile. If unknown, returns baseline capacities.
        """
        # Case insensitive lookup
        for key, value in cls._registry.items():
            if key.lower() in model_name.lower():
                return value
        # Baseline fallback for unknown local/custom models
        return ModelCapabilities(chat=True, json_mode=False, tool_use=False, long_context=False, reasoning_stability="medium")
