from sqlalchemy import String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class MultimodalIngestLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "multimodal_ingest_logs"

    workflow_run_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    media_type: Mapped[str] = mapped_column(String(50), nullable=False)  # screenshot, document, voice_transcript, text
    raw_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=True)
    detected_entities: Mapped[dict] = mapped_column(JSON, default=dict)
    safety_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
