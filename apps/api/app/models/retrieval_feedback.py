from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class RetrievalFeedback(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "retrieval_feedbacks"

    trace_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 for positive, -1 for negative
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
