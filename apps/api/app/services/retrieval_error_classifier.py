class RetrievalErrorClassifier:
    @classmethod
    def classify_failure(cls, exception: Exception) -> str:
        """
        Classifies database/retrieval errors into standardized diagnostic labels.
        """
        message = str(exception).lower()
        if "permission" in message or "access" in message:
            return "tenant_boundary_violation"
        if "timeout" in message:
            return "provider_timeout_failure"
        return "internal_query_exception"
