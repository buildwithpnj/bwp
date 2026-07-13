from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from typing import List
from app.deps import CurrentUser, DB
from app.models.notification_event import NotificationEvent
from app.schemas.notification_payload import NotificationPayload
from app.schemas.notification_action import NotificationAction
from app.services.notification_dispatch_service import NotificationDispatchService
from app.services.notification_action_router import NotificationActionRouter

router = APIRouter(prefix="/api/notifications", tags=["Active Intervention Alerts"])

@router.get("/feed", status_code=status.HTTP_200_OK)
async def get_notification_feed(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns lists of alert notifications for active dashboard feed overlays.
    """
    stmt = select(NotificationEvent).where(
        NotificationEvent.user_id == current_user.id
    ).order_by(NotificationEvent.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/dispatch", status_code=status.HTTP_201_CREATED)
async def dispatch_new_alert(
    payload: NotificationPayload,
    current_user: CurrentUser,
    db: DB
):
    """
    Manually schedules a new notification alert.
    """
    event = await NotificationDispatchService.dispatch_notification(db, current_user.id, payload)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notification blocked as duplicate."
        )
    return event

@router.post("/{notification_id}/action", status_code=status.HTTP_200_OK)
async def execute_notification_action(
    notification_id: str,
    action: NotificationAction,
    current_user: CurrentUser,
    db: DB
):
    """
    Routes an action from a notification card.
    """
    # Verify ownership
    stmt = select(NotificationEvent).where(
        NotificationEvent.id == notification_id,
        NotificationEvent.user_id == current_user.id
    )
    res = await db.execute(stmt)
    event = res.scalar_one_or_none()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found."
        )
        
    success = await NotificationActionRouter.route_notification_action(db, notification_id, action)
    if success:
        event.status = "read"
        await db.commit()
        return {"status": "executed"}
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Action execution failed."
    )

@router.post("/{notification_id}/dismiss", status_code=status.HTTP_200_OK)
async def dismiss_notification(
    notification_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Dismisses notification alert to remove it from feed overlays.
    """
    stmt = select(NotificationEvent).where(
        NotificationEvent.id == notification_id,
        NotificationEvent.user_id == current_user.id
    )
    res = await db.execute(stmt)
    event = res.scalar_one_or_none()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found."
        )
        
    event.status = "dismissed"
    await db.commit()
    return {"status": "dismissed"}
