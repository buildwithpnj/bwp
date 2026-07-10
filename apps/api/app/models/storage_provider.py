from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class StorageProvider(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "storage_providers"

    # ── Identity ──────────────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_label: Mapped[str | None] = mapped_column(String(10), nullable=True)   # "A", "B", "C"
    type: Mapped[str] = mapped_column(String(50), nullable=False)                   # 'google_drive', 's3', etc.
    account_email: Mapped[str] = mapped_column(String(255), nullable=False)

    # ── Per-Provider OAuth Credentials (stored in DB for multi-app support) ───
    # client_id is non-secret; stored plain text
    client_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # client_secret is secret; stored Fernet-encrypted
    encrypted_client_secret: Mapped[str | None] = mapped_column(Text, nullable=True)
    # redirect_uri may differ per provider / environment
    redirect_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # ── Token Storage ─────────────────────────────────────────────────────────
    encrypted_refresh_token: Mapped[str] = mapped_column(Text, nullable=False)
    drive_folder_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ── Operational State ─────────────────────────────────────────────────────
    status: Mapped[str] = mapped_column(String(50), default="active")   # 'active', 'error', 'offline'
    priority: Mapped[int] = mapped_column(Integer, default=0)            # Lower = higher priority

    # ── Quota Tracking ────────────────────────────────────────────────────────
    used_storage: Mapped[int] = mapped_column(BigInteger, default=0)
    available_storage: Mapped[int] = mapped_column(BigInteger, default=0)
    last_sync: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
