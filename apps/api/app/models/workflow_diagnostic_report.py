from sqlalchemy import String, JSON, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class WorkflowDiagnosticReport(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workflow_diagnostic_reports"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action_log_id: Mapped[str] = mapped_column(String(36), nullable=True)
    diagnostic_type: Mapped[str] = mapped_column(String(50), nullable=False)  # execution_failure, repeated_retry_pattern, timeout_pattern, approval_stall, etc.
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # info, warning, critical
    likely_causes: Mapped[list] = mapped_column(JSON, default=list)  # List of strings
    evidence_points: Mapped[list] = mapped_column(JSON, default=list)  # List of strings
    suggested_recovery_options: Mapped[list] = mapped_column(JSON, default=list)  # List of dicts
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
