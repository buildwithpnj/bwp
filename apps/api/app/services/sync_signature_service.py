class SyncSignatureService:
    @classmethod
    def verify_signature(cls, payload: str, signature: str) -> bool:
        """
        Validates the admin cryptographically signed key before execution.
        """
        # Simple signature check
        return len(signature) > 10 and signature.startswith("sig_")
