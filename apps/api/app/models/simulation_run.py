from sqlalchemy import String, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class SimulationRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "simulation_runs"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    plan_steps: Mapped[dict] = mapped_column(JSON, default=dict)
    predicted_success_score: Mapped[float] = mapped_column(Float, default=1.0)
    likely_failures: Mapped[list] = mapped_column(JSON, default=list)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
