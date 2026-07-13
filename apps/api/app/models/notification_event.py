from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class NotificationEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_events"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # workflow_failure, objective_checkpoint, quota_exceeded
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")  # high, medium, low
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="unread")  # unread, read, dismissed
