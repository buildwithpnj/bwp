import re

class MemoryWritePolicy:
    # Patterns for sensitive/unsafe keywords to reject profile writes
    SENSITIVE_PATTERNS = [
        r"password",
        r"secret",
        r"api_key",
        r"private_key",
        r"token",
        r"credit_card",
        r"social_security",
        r"ssn",
        r"bank_account"
    ]

    @classmethod
    def can_write_profile(cls, user_role: str, updates: dict) -> bool:
        """Enforces write access control: block anonymous profiles and sensitive terms."""
        if user_role not in ["approved_user", "internal_admin"]:
            return False
            
        for key, val in updates.items():
            str_val = str(val).lower()
            for pattern in cls.SENSITIVE_PATTERNS:
                if re.search(pattern, str_val):
                    return False
        return True
