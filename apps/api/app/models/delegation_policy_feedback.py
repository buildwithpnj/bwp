from sqlalchemy import String, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class DelegationPolicyFeedback(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "delegation_policy_feedbacks"

    specialist_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    workflow_type: Mapped[str] = mapped_column(String(50), nullable=False)
    usefulness_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)  # 0.0 (wasteful) to 1.0 (highly useful)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    token_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    user_interventions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    was_successful: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
