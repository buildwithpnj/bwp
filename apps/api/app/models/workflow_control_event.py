from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base, TimestampMixin, UUIDMixin

class WorkflowControlEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workflow_control_events"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action_log_id: Mapped[str] = mapped_column(String(36), nullable=True)
    control_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pause_workflow, resume_workflow, cancel_workflow, approve_checkpoint, replay_failed_step
    requested_by_user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    requested_by_role: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    result_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # applied, rejected, error
