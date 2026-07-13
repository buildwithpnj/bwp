from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class FederatedRollbackBundle(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "federated_rollback_bundles"

    job_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    snapshot_data: Mapped[str] = mapped_column(Text, nullable=False)
