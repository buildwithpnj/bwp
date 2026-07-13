class IngestBackpressureService:
    @classmethod
    def should_degrade_to_async_queue(cls, active_queue_depth: int) -> bool:
        """
        Determines if synchronous endpoint queries should degrade to async worker queues.
        """
        # Capped at 5 active uploads
        return active_queue_depth > 5
