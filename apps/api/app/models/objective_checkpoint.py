from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ObjectiveCheckpoint(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "objective_checkpoints"

    objective_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, verified, failed
