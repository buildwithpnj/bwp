from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class AnomalyCorrelationLink(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "anomaly_correlation_links"

    parent_incident_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    child_incident_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
