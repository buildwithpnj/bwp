import pytest
from unittest.mock import AsyncMock
from app.services.notification_dispatch_service import NotificationDispatchService
from app.schemas.notification_payload import NotificationPayload
from app.services.notification_dedup_service import NotificationDedupService

@pytest.mark.asyncio
async def test_notification_deduplication_and_priority():
    db = AsyncMock()
    
    # 1. Reset dedup cache
    NotificationDedupService._last_sent.clear()
    
    payload = NotificationPayload(
        source_type="workflow_failure",
        title="Workflow wf_abc failed",
        description="Missing parameters",
        priority="medium"
    )
    
    # First dispatch should succeed
    evt = await NotificationDispatchService.dispatch_notification(db, "usr_123", payload)
    assert evt is not None
    assert evt.priority == "high"  # Inferred priority
    
    # Second dispatch is immediately filtered as duplicate
    evt2 = await NotificationDispatchService.dispatch_notification(db, "usr_123", payload)
    assert evt2 is None
