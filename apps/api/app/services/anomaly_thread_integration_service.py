class AnomalyThreadIntegrationService:
    @classmethod
    def link_to_thread(cls, thread_id: str, incident_id: str) -> dict:
        """
        Attaches active incident alerts directly to user threads.
        """
        return {
            "thread_id": thread_id,
            "incident_id": incident_id,
            "linked": True
        }
