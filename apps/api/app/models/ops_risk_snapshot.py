from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class OpsRiskSnapshot(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ops_risk_snapshots"

    tenant_scope: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    cluster_scope: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    recommended_prevention: Mapped[str] = mapped_column(Text, nullable=True)
