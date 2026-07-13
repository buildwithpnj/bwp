from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class ThreadContextLink(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "thread_context_links"

    operating_thread_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    linked_entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # workflow_run, objective_run
    linked_entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
