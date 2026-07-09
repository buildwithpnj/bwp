import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = (
        "postgresql+asyncpg://personal_os:personal_os_dev@localhost:5432/personal_os"
    )

    def __init__(self, **values):
        super().__init__(**values)
        # Robust fallback: fetch directly from host environment variables
        env_db_url = (
            os.environ.get("DATABASE_URL") or 
            os.environ.get("DATABASE_PRIVATE_URL") or 
            os.environ.get("database_url")
        )
        if env_db_url:
            self.database_url = env_db_url

        if self.database_url:
            from urllib.parse import urlparse, urlunparse, quote, unquote
            try:
                # Clean trailing/leading whitespace and quotes
                raw_url = self.database_url.strip().strip('"').strip("'")
                parsed = urlparse(raw_url)
                scheme = parsed.scheme
                
                # Standardize scheme for asyncpg
                if scheme in ("postgres", "postgresql"):
                    scheme = "postgresql+asyncpg"
                    
                netloc = parsed.netloc
                if '@' in netloc:
                    userinfo, hostinfo = netloc.rsplit('@', 1)
                    if ':' in userinfo:
                        username, password = userinfo.split(':', 1)
                        # URL-encode username and password safely to prevent special character parse issues
                        username = quote(unquote(username))
                        password = quote(unquote(password))
                        userinfo = f"{username}:{password}"
                    else:
                        userinfo = quote(unquote(userinfo))
                    netloc = f"{userinfo}@{hostinfo}"
                    
                # Reconstruct standardized URL
                self.database_url = urlunparse((
                    scheme,
                    netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
            except Exception:
                # Fallback: simple prefix replacement if urllib parsing fails
                self.database_url = self.database_url.strip().strip('"').strip("'")
                if self.database_url.startswith("postgres://"):
                    self.database_url = self.database_url.replace("postgres://", "postgresql+asyncpg://", 1)
                elif self.database_url.startswith("postgresql://"):
                    self.database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    jwt_secret: str = "change-me-to-a-random-64-char-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Google Drive Integration
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str = "http://localhost:3000/storage/callback"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000"


settings = Settings()
