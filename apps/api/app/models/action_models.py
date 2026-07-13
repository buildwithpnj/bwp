from sqlalchemy import String, ForeignKey, JSON, Boolean, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
from datetime import datetime

class ActionDefinition(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "action_definitions"

    action_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    allowed_roles: Mapped[list] = mapped_column(JSON, default=list)  # list of allowed roles e.g. ["approved_user", "internal_admin"]
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")

class ActionLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "action_logs"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=True)
    action_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    input_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    result_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, success, failed
    approval_status: Mapped[str] = mapped_column(String(50), default="auto_approved")  # auto_approved, pending, approved, rejected
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # V15 Lifecycle and Reliability columns
    suggested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    queued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    execution_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rolled_back_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)
    
    execution_status: Mapped[str] = mapped_column(String(50), default="suggested", nullable=False)
    recovery_status: Mapped[str] = mapped_column(String(50), default="none", nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=True, index=True)

    # V16 Queue/Worker columns
    queued_job_id: Mapped[str] = mapped_column(String(255), nullable=True)
    queue_name: Mapped[str] = mapped_column(String(255), nullable=True)
    worker_id: Mapped[str] = mapped_column(String(255), nullable=True)
    retry_scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    dead_lettered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    execution_source: Mapped[str] = mapped_column(String(50), default="api", nullable=False)

class ActionApproval(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "action_approvals"

    action_log_id: Mapped[str] = mapped_column(String(36), ForeignKey("action_logs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, approved, rejected, expired
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
