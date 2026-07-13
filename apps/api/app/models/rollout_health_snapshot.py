from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class RolloutHealthSnapshot(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "rollout_health_snapshots"

    rollout_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    health_score: Mapped[float] = mapped_column(Float, default=1.0)
    status_summary: Mapped[str] = mapped_column(Text, nullable=True)
