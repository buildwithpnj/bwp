import os

class AgentConfig:
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = "gpt-4o-mini"
    
    # Public Preview Intent Constraints
    ALLOWED_PREVIEW_INTENTS = [
        "english_correction",
        "rewrite",
        "hinglish_to_english",
        "explanation"
    ]
    
    # Public Preview Hard Constraints
    MAX_TURNS_PER_SESSION = 5
    MAX_OUTPUT_LENGTH = 300
    TOKEN_BUDGET_PER_SESSION = 2000
    TOKEN_BUDGET_PER_DAY = 50000
    
    # Fallback message
    BUDGET_EXCEEDED_FALLBACK = (
        "You have reached the preview limit. Please sign in or request "
        "full developer credentials to access the unrestricted Warborn system."
    )
