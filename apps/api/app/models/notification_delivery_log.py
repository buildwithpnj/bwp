from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class NotificationDeliveryLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_delivery_logs"

    notification_event_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)  # in_app, desktop
    delivered_at: Mapped[str] = mapped_column(DateTime, nullable=True)
