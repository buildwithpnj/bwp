import base64
import hashlib
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Provider A — Global OAuth App ─────────────────────────────────────────
    google_client_id: str | None = Field(default=None, validation_alias="GOOGLE_CLIENT_ID")
    google_client_secret: str | None = Field(default=None, validation_alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(
        default="http://localhost:3000/storage/callback",
        validation_alias="GOOGLE_REDIRECT_URI"
    )

    # ── Provider B — Separate OAuth App ───────────────────────────────────────
    google_drive_b_client_id: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_B_CLIENT_ID")
    google_drive_b_client_secret: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_B_CLIENT_SECRET")
    google_drive_b_redirect_uri: str = Field(
        default="http://localhost:3000/auth/google/callback",
        validation_alias="GOOGLE_DRIVE_B_REDIRECT_URI"
    )

    # ── Provider C — Separate OAuth App (reserved) ────────────────────────────
    google_drive_c_client_id: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_C_CLIENT_ID")
    google_drive_c_client_secret: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_C_CLIENT_SECRET")
    google_drive_c_redirect_uri: str = Field(
        default="http://localhost:3000/storage/callback",
        validation_alias="GOOGLE_DRIVE_C_REDIRECT_URI"
    )

    # ── Seed Refresh Tokens (optional, for auto-seeding on first boot) ────────
    google_drive_a_refresh_token: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_A_REFRESH_TOKEN")
    google_drive_b_refresh_token: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_B_REFRESH_TOKEN")
    google_drive_c_refresh_token: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_C_REFRESH_TOKEN")

    google_drive_a_folder_id: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_A_FOLDER_ID")
    google_drive_b_folder_id: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_B_FOLDER_ID")
    google_drive_c_folder_id: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_C_FOLDER_ID")

    google_drive_a_email: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_A_EMAIL")
    google_drive_b_email: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_B_EMAIL")
    google_drive_c_email: str | None = Field(default=None, validation_alias="GOOGLE_DRIVE_C_EMAIL")

    # ── Encryption ────────────────────────────────────────────────────────────
    raw_encryption_key: str = Field(
        default="production-secret-encryption-key-must-change-to-something-secure-for-warborn-os",
        validation_alias="ENCRYPTION_KEY"
    )

    @property
    def encryption_key(self) -> bytes:
        """Derive a stable 32-byte URL-safe base64 Fernet key from ENCRYPTION_KEY string."""
        hashed = hashlib.sha256(self.raw_encryption_key.encode()).digest()
        return base64.urlsafe_b64encode(hashed)


storage_settings = StorageSettings()
