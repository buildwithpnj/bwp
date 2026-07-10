import sys
import logging
from urllib.parse import urlparse

logger = logging.getLogger("warborn_config_validator")


def validate_config() -> None:
    """Validate all required settings on startup using the already-loaded StorageSettings.
    Fails fast if formats or values are invalid.
    """
    # Import the already-parsed settings object (reads .env file via pydantic-settings)
    from app.storage.config import storage_settings
    from app.config import settings as app_settings

    errors = []

    # 1. Required Variables Presence Check (via parsed settings, not raw os.environ)
    if not storage_settings.google_client_id:
        errors.append("Missing: GOOGLE_CLIENT_ID")
    if not storage_settings.google_client_secret:
        errors.append("Missing: GOOGLE_CLIENT_SECRET")
    if not app_settings.database_url:
        errors.append("Missing: DATABASE_URL")
    if not app_settings.redis_url:
        errors.append("Missing: REDIS_URL")
    if not storage_settings.raw_encryption_key:
        errors.append("Missing: ENCRYPTION_KEY")

    # 2. Format & Value Validations
    if app_settings.database_url:
        try:
            parsed = urlparse(str(app_settings.database_url))
            if parsed.scheme not in ("postgres", "postgresql", "postgresql+asyncpg"):
                errors.append(f"Invalid DATABASE_URL scheme '{parsed.scheme}'. Must be postgresql.")
        except Exception as e:
            errors.append(f"DATABASE_URL parse error: {e}")

    if app_settings.redis_url:
        try:
            parsed = urlparse(str(app_settings.redis_url))
            if parsed.scheme not in ("redis", "rediss"):
                errors.append(f"Invalid REDIS_URL scheme '{parsed.scheme}'. Must be redis or rediss.")
        except Exception as e:
            errors.append(f"REDIS_URL parse error: {e}")

    if storage_settings.raw_encryption_key and len(storage_settings.raw_encryption_key) < 16:
        errors.append("ENCRYPTION_KEY is too short. Must be at least 16 characters.")

    # Fail fast if there are validation errors
    if errors:
        print("\n" + "="*80, file=sys.stderr)
        print("FATAL CONFIGURATION ERROR - WARBORN OS STARTUP CANCELLED", file=sys.stderr)
        print("="*80, file=sys.stderr)
        for err in errors:
            print(f"[-] {err}", file=sys.stderr)
        print("="*80 + "\n", file=sys.stderr)
        raise RuntimeError("Startup validation failed: Invalid configuration environment.")

    # 3. Print startup report (safely) using ASCII — no secrets exposed
    print("\n" + "="*60)
    print(" BUILDWITHPNJ PROJECT OPERATING SYSTEM - STARTUP REPORT")
    print("="*60)

    client_id = storage_settings.google_client_id or ""
    masked_client = client_id[:10] + "..." if len(client_id) > 10 else "not configured"
    print(f" [System] OAuth Client ID:  {masked_client}")

    drives = [
        ("A", storage_settings.google_drive_a_email, storage_settings.google_drive_a_refresh_token, storage_settings.google_drive_a_folder_id),
        ("B", storage_settings.google_drive_b_email, storage_settings.google_drive_b_refresh_token, storage_settings.google_drive_b_folder_id),
        ("C", storage_settings.google_drive_c_email, storage_settings.google_drive_c_refresh_token, storage_settings.google_drive_c_folder_id),
    ]
    for label, email, token, folder in drives:
        status = "ACTIVE" if (email and token) else "NOT CONFIGURED"
        email_str = email if email else "N/A"
        folder_str = folder if folder else "root"
        print(f" [Drive]  Google Drive {label}:  {status} ({email_str} | Folder: {folder_str})")

    print(" [Crypto] Key Status:      Fernet AES encryption activated")
    print("="*60 + "\n")
