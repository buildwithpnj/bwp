from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Addiction(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "user_addictions"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quit_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cost_per_day: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    time_saved_per_day_mins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    relapses: Mapped[list["RelapseLog"]] = relationship(
        back_populates="addiction", cascade="all, delete-orphan"
    )


class RelapseLog(Base, UUIDMixin):
    __tablename__ = "relapse_logs"

    addiction_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user_addictions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relapsed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    trigger_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    mood_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)

    addiction: Mapped["Addiction"] = relationship(back_populates="relapses")
