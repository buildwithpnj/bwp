from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin

class PatternRegressionCase(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "pattern_regression_cases"

    pattern_family: Mapped[str] = mapped_column(String(100), nullable=False)
    regression_score: Mapped[float] = mapped_column(Float, default=0.0)
