from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class TelemetryEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "telemetry_events"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(50), nullable=False)
    service_name: Mapped[str] = mapped_column(String(50), nullable=False)
    environment: Mapped[str] = mapped_column(String(50), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(20), nullable=False)  # log, metric, event
    payload: Mapped[str] = mapped_column(Text, nullable=True)
