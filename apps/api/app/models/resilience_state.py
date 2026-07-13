from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ResilienceState(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resilience_states"

    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)
    affected_scope: Mapped[str] = mapped_column(String(100), nullable=False)
    degradation_level: Mapped[str] = mapped_column(String(20), nullable=False, default="normal")  # normal, degraded, critical
    token_budget_reduction_factor: Mapped[float] = mapped_column(Float, default=1.0)
