from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class UserProfileMemory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "user_profile_memories"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    tone: Mapped[str] = mapped_column(String(50), default="professional")  # professional, conversational, concise
    explanation_style: Mapped[str] = mapped_column(String(50), default="detailed")  # detailed, brief, rule-based
    target_english_level: Mapped[str] = mapped_column(String(50), default="Advanced")
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)  # list of strings e.g. ["prepositions", "tense consistency"]
    goals: Mapped[list] = mapped_column(JSON, default=list)  # list of strings e.g. ["business writing", "clear emails"]
    preferred_language: Mapped[str] = mapped_column(String(50), default="English")  # English, Hindi, Hinglish
