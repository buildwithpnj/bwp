from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class PredictiveIncidentSignal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "predictive_incident_signals"

    pattern_family: Mapped[str] = mapped_column(String(100), nullable=False)
    leading_signals: Mapped[str] = mapped_column(Text, nullable=False)
    projected_impact: Mapped[str] = mapped_column(Text, nullable=True)
