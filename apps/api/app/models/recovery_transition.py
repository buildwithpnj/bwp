from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class RecoveryTransition(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "recovery_transitions"

    affected_scope: Mapped[str] = mapped_column(String(100), nullable=False)
    recovery_status: Mapped[str] = mapped_column(String(20), nullable=False, default="completed")  # started, completed
