from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class KnowledgeIndexRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_index_runs"

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="started")  # started, completed, failed
    documents_added: Mapped[int] = mapped_column(Integer, default=0)
    chunks_created: Mapped[int] = mapped_column(Integer, default=0)
