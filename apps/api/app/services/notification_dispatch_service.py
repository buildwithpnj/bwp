import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.notification_event import NotificationEvent
from app.models.notification_delivery_log import NotificationDeliveryLog
from app.schemas.notification_payload import NotificationPayload
from app.services.notification_dedup_service import NotificationDedupService
from app.services.notification_priority_service import NotificationPriorityService

class NotificationDispatchService:
    @classmethod
    async def dispatch_notification(
        cls,
        db: AsyncSession,
        user_id: str,
        payload: NotificationPayload
    ) -> Optional[NotificationEvent]:
        """
        Dispatches new intervention notification alerts, filtering spams and logging channels.
        """
        # 1. Deduplication check
        if NotificationDedupService.is_duplicate(user_id, payload.title):
            return None
            
        priority = NotificationPriorityService.infer_priority(payload.source_type)
        
        # 2. Persist notification
        evt_id = str(uuid.uuid4())
        event = NotificationEvent(
            id=evt_id,
            user_id=user_id,
            source_type=payload.source_type,
            title=payload.title,
            description=payload.description,
            priority=priority,
            status="unread"
        )
        db.add(event)
        
        # Log delivery channel
        delivery = NotificationDeliveryLog(
            id=str(uuid.uuid4()),
            notification_event_id=evt_id,
            channel="in_app"
        )
        db.add(delivery)
        
        await db.commit()
        return event
