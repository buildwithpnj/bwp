from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class CanaryRollout(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "canary_rollouts"

    rollout_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    canary_percentage: Mapped[int] = mapped_column(Integer, default=10)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")  # active, paused, completed, rolled_back
