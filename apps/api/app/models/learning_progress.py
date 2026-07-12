from sqlalchemy import String, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class LearningProgress(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "learning_progresses"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    corrections_accepted: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    mastered_patterns: Mapped[list] = mapped_column(JSON, default=list)  # list of strings
    weak_categories: Mapped[list] = mapped_column(JSON, default=list)  # list of strings
    prompt_categories_used: Mapped[list] = mapped_column(JSON, default=list)  # list of strings
    return_frequency: Mapped[int] = mapped_column(Integer, default=1)
