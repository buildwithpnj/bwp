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

llm_settings = LLMSettings()
