from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class PolicySyncTarget(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "policy_sync_targets"

    job_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    node_ip: Mapped[str] = mapped_column(String(50), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
