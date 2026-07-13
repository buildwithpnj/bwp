from sqlalchemy import String, JSON, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class WorkflowRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workflow_runs"

    goal: Mapped[str] = mapped_column(String(500), nullable=True)
    reasoning_summary: Mapped[str] = mapped_column(Text, nullable=True)
    steps: Mapped[list] = mapped_column(JSON, default=list)  # List of dict steps, e.g. [{"action_name": "...", "payload": {...}}]
    current_step_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, executing, paused_approval, succeeded, failed
    autonomy_tier: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
