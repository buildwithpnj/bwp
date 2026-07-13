import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: str = Field(default="openai", validation_alias="llm_provider")
    ollama_base_url: str = Field(default="http://localhost:11434", validation_alias="ollama_base_url")
    ollama_model: str = Field(default="llama3", validation_alias="ollama_model")
    ollama_timeout_seconds: int = Field(default=120, validation_alias="ollama_timeout_seconds")
    
    openai_api_key: str | None = Field(default=None, validation_alias="openai_api_key")
    gemini_api_key: str | None = Field(default=None, validation_alias="gemini_api_key")

    # Additive local validation & safety controls (V45-H)
    local_ai_enabled: bool = Field(default=True, validation_alias="local_ai_enabled")
    provider_fallback_enabled: bool = Field(default=True, validation_alias="provider_fallback_enabled")
    primary_cloud_provider: str = Field(default="openai", validation_alias="primary_cloud_provider")
    
    loop_max_steps: int = Field(default=5, validation_alias="loop_max_steps")
    loop_max_retries: int = Field(default=3, validation_alias="loop_max_retries")
    
    grounding_guard_enabled: bool = Field(default=True, validation_alias="grounding_guard_enabled")
    approval_gates_enabled: bool = Field(default=True, validation_alias="approval_gates_enabled")
    idempotency_guard_enabled: bool = Field(default=True, validation_alias="idempotency_guard_enabled")
    tenant_guards_enabled: bool = Field(default=True, validation_alias="tenant_guards_enabled")
    
    confidence_collapse_protection: bool = Field(default=True, validation_alias="confidence_collapse_protection")
    no_progress_stop_enabled: bool = Field(default=True, validation_alias="no_progress_stop_enabled")

llm_settings = LLMSettings()
