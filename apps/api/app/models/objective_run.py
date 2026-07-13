from sqlalchemy import String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ObjectiveRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "objective_runs"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="active")  # active, completed, paused
    stop_condition: Mapped[str] = mapped_column(String(255), nullable=True)
