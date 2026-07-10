from cryptography.fernet import Fernet
from app.storage.config import storage_settings


def encrypt_token(token: str) -> str:
    """Encrypt a plaintext token string using the derived Fernet key."""
    if not token:
        return ""
    f = Fernet(storage_settings.encryption_key)
    return f.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a ciphertext token string back to plaintext using the derived Fernet key."""
    if not encrypted_token:
        return ""
    f = Fernet(storage_settings.encryption_key)
    return f.decrypt(encrypted_token.encode()).decode()
