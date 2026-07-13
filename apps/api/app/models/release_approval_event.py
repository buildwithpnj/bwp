from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ReleaseApprovalEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "release_approval_events"

    rollout_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    approved_by_user_id: Mapped[str] = mapped_column(String(36), nullable=False)
