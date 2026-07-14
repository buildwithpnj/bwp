import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone

class ApprovalTokenService:
    # In-memory store for active tokens to allow stateless verification
    # Maps: token_str -> {approval_id, user_id, tenant_id, expires_at}
    _token_cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def generate_token(
        cls, 
        approval_id: str, 
        user_id: str, 
        tenant_id: Optional[str] = None, 
        expiry_seconds: int = 300
    ) -> str:
        """
        Generates a secure, single-use approval token bound to user, tenant, and approval request.
        """
        token = f"tok_{secrets.token_urlsafe(32)}"
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
        
        cls._token_cache[token] = {
            "approval_id": approval_id,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "expires_at": expires_at
        }
        return token

    @classmethod
    def validate_and_burn_token(
        cls, 
        token: str, 
        user_id: str, 
        tenant_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Validates token bounds (user, tenant, expiration). If valid, burns the token (removes it)
        to prevent replay attacks, and returns the bound approval_id.
        """
        token_data = cls._token_cache.get(token)
        if not token_data:
            return None

        # Verify expiration
        if datetime.now(timezone.utc) > token_data["expires_at"]:
            cls._token_cache.pop(token, None)
            return None

        # Verify user alignment
        if token_data["user_id"] != user_id:
            return None

        # Verify tenant scope alignment
        if token_data["tenant_id"] != tenant_id:
            return None

        # Burn the token on first validation attempt (single-use constraint)
        cls._token_cache.pop(token, None)
        return token_data["approval_id"]

    @classmethod
    def clear_expired_tokens(cls):
        now = datetime.now(timezone.utc)
        expired = [t for t, data in cls._token_cache.items() if now > data["expires_at"]]
        for t in expired:
            cls._token_cache.pop(t, None)
