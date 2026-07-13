from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class TenantAlertRule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenant_alert_rules"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_muted: Mapped[bool] = mapped_column(Boolean, default=False)
