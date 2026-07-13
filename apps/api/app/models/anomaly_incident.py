from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
import datetime

class AnomalyIncident(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "anomaly_incidents"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    incident_status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")  # active, acknowledged, resolved
    correlation_key: Mapped[str] = mapped_column(String(100), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    resolved_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
