import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pattern_regression_case import PatternRegressionCase

class PatternDetectionService:
    @classmethod
    async def log_regression_pattern(
        cls,
        db: AsyncSession,
        family: str,
        score: float
    ) -> PatternRegressionCase:
        """
        Stores repeating risk signature occurrences.
        """
        item = PatternRegressionCase(
            id=str(uuid.uuid4()),
            pattern_family=family,
            regression_score=score
        )
        db.add(item)
        await db.commit()
        return item
