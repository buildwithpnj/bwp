from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ReleaseGate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "release_gates"

    rollout_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    gate_type: Mapped[str] = mapped_column(String(50), nullable=False)  # manual_approval, metric_health
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending, passed, failed
