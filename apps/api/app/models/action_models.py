from sqlalchemy import String, ForeignKey, JSON, Boolean, Text, DateTime
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

class ActionApproval(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "action_approvals"

    action_log_id: Mapped[str] = mapped_column(String(36), ForeignKey("action_logs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, approved, rejected, expired
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
