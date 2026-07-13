from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ContextCompactionRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "context_compaction_runs"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    raw_tokens_count: Mapped[int] = mapped_column(Integer, nullable=False)
    compacted_tokens_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reduction_ratio: Mapped[float] = mapped_column(Float, nullable=False)
