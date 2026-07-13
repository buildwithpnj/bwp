from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class CollaborationHandoff(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "collaboration_handoffs"

    collaboration_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    sender_agent: Mapped[str] = mapped_column(String(50), nullable=False)
    receiver_agent: Mapped[str] = mapped_column(String(50), nullable=False)
    payload_contract: Mapped[dict] = mapped_column(JSON, default=dict)
    handoff_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # pending, accepted, rejected
