import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Database
    database_url_env: str = Field(
        default="postgresql+asyncpg://personal_os:personal_os_dev@localhost:5432/personal_os",
        validation_alias="database_url",
    )

    @property
    def database_url(self) -> str:
        # Fallback to direct environment check
        url = (
            os.environ.get("DATABASE_URL") or 
            os.environ.get("DATABASE_PRIVATE_URL") or 
            self.database_url_env
        )
        if not url:
            return url

        # Clean trailing/leading whitespace and quotes
        url = url.strip().strip('"').strip("'")
        
        # Strip literal prefixes like "DATABASE_URL=" or "DATABASE_PRIVATE_URL="
        for prefix in ("database_url=", "database_private_url="):
            if url.lower().startswith(prefix):
                url = url[len(prefix):]
                url = url.strip().strip('"').strip("'")
        
        from urllib.parse import urlparse, urlunparse, quote, unquote
        try:
            parsed = urlparse(url)
            scheme = parsed.scheme
            
            # Standardize scheme for asyncpg
            if scheme in ("postgres", "postgresql"):
                scheme = "postgresql+asyncpg"
                
            netloc = parsed.netloc
            if '@' in netloc:
                userinfo, hostinfo = netloc.rsplit('@', 1)
                if ':' in userinfo:
                    username, password = userinfo.split(':', 1)
                    # URL-encode username and password safely
                    username = quote(unquote(username))
                    password = quote(unquote(password))
                    userinfo = f"{username}:{password}"
                else:
                    userinfo = quote(unquote(userinfo))
                netloc = f"{userinfo}@{hostinfo}"
                
            # Reconstruct standardized URL
            return urlunparse((
                scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
        except Exception:
            # Fallback simple replacement if parsing fails
            if url.startswith("postgres://"):
                return url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                return url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url



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
