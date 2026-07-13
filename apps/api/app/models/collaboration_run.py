from sqlalchemy import String, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class CollaborationRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "collaboration_runs"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    participating_agents: Mapped[list] = mapped_column(JSON, default=list)  # List of agent names
    coordination_status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")  # active, merged, failed
    max_total_steps: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    max_parallel_branches: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
