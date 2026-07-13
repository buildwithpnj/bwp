from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class GovernancePolicyChange(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "governance_policy_changes"

    changed_by_user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    target_tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    old_value: Mapped[str] = mapped_column(Text, nullable=True)
    new_value: Mapped[str] = mapped_column(Text, nullable=True)
