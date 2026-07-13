from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class PolicySyncResult(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "policy_sync_results"

    target_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
