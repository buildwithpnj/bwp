from sqlalchemy import String, JSON, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
from datetime import datetime

class ActionApprovalRequest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "action_approval_requests"

    action_log_id: Mapped[str] = mapped_column(String(36), ForeignKey("action_logs.id", ondelete="CASCADE"), nullable=True)
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(255), nullable=True)
    
    action_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    module_name: Mapped[str] = mapped_column(String(255), nullable=True)
    policy_tier: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)  # safe, medium, high, critical
    
    target_type: Mapped[str] = mapped_column(String(255), nullable=True)
    target_id: Mapped[str] = mapped_column(String(255), nullable=True)
    action_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    human_summary: Mapped[str] = mapped_column(Text, nullable=True)
    execution_preview: Mapped[str] = mapped_column(Text, nullable=True)
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending | approved | denied | expired | executed | cancelled
    
    approved_by: Mapped[str] = mapped_column(String(36), nullable=True)
    denied_by: Mapped[str] = mapped_column(String(36), nullable=True)
    audit_id: Mapped[str] = mapped_column(String(255), nullable=True)
