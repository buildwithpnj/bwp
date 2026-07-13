from sqlalchemy import String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class TenantModalityQuota(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenant_modality_quotas"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    daily_bytes_limit: Mapped[int] = mapped_column(BigInteger, default=52428800)  # 50 MB
    daily_bytes_used: Mapped[int] = mapped_column(BigInteger, default=0)
    requests_count_limit: Mapped[int] = mapped_column(Integer, default=100)
    requests_count_used: Mapped[int] = mapped_column(Integer, default=0)
