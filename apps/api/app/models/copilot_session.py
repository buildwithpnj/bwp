from sqlalchemy import String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class CopilotSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "copilot_sessions"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    chat_history: Mapped[list] = mapped_column(JSON, default=list)  # List of message dicts
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
