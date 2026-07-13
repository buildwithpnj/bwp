from sqlalchemy import String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class DelegationRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "delegation_runs"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action_log_id: Mapped[str] = mapped_column(String(36), nullable=True)
    parent_step_id: Mapped[str] = mapped_column(String(36), nullable=True)
    requesting_agent: Mapped[str] = mapped_column(String(50), nullable=False)
    specialist_type: Mapped[str] = mapped_column(String(50), nullable=False)
    delegation_reason: Mapped[str] = mapped_column(Text, nullable=False)
    bounded_goal: Mapped[str] = mapped_column(Text, nullable=False)
    outcome_status: Mapped[str] = mapped_column(String(50), nullable=False, default="delegated")
    reasoning_summary: Mapped[str] = mapped_column(Text, nullable=True)
    structured_findings: Mapped[dict] = mapped_column(JSON, default=dict)
    suggested_next_step: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    token_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
