from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class DegradedModeActivation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "degraded_mode_activations"

    affected_scope: Mapped[str] = mapped_column(String(100), nullable=False)
    activated_features: Mapped[str] = mapped_column(Text, nullable=True)
    disabled_features: Mapped[str] = mapped_column(Text, nullable=True)
