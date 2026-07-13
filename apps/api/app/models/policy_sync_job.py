from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class PolicySyncJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "policy_sync_jobs"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    source_env: Mapped[str] = mapped_column(String(50), nullable=False)
    target_env: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="preview")  # preview, applied, failed
    signature: Mapped[str] = mapped_column(String(255), nullable=True)
