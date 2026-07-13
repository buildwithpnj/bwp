class NotificationPriorityService:
    @classmethod
    def infer_priority(cls, source_type: str) -> str:
        """
        Categorizes notifications priorities based on critical threat levels.
        """
        critical_sources = {"workflow_failure", "quota_exceeded", "operational_anomaly"}
        if source_type in critical_sources:
            return "high"
        return "medium"
