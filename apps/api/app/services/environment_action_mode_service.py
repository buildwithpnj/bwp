import os
from app.config import settings
from app.runtime_mode import RuntimeMode

class EnvironmentActionModeService:
    @classmethod
    def get_runtime_mode(cls) -> RuntimeMode:
        """
        Detects runtime environment and returns target execution routing mode.
        """
        mode_str = os.getenv("RUNTIME_MODE", "").upper()
        if mode_str in RuntimeMode.__members__:
            return RuntimeMode[mode_str]
            
        # Default fallback logic based on LLM provider configuration
        if os.getenv("LLM_PROVIDER") == "ollama":
            return RuntimeMode.LIVE_SYNC
        return RuntimeMode.LOCAL_SYNC
