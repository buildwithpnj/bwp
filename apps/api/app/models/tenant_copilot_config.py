from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class TenantCopilotConfig(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenant_copilot_configs"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    voice_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    proactive_tips_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
