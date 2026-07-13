from sqlalchemy import String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class RetrievalTrace(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "retrieval_traces"

    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    rewritten_query: Mapped[str] = mapped_column(Text, nullable=True)
    strategy_used: Mapped[str] = mapped_column(String(50), nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
