import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.retrieval_feedback import RetrievalFeedback

class RetrievalFeedbackService:
    @classmethod
    async def record_feedback(
        cls,
        db: AsyncSession,
        trace_id: str,
        score: int,
        notes: str = None
    ) -> RetrievalFeedback:
        """
        Stores user feedback metrics in db for reinforcement learning.
        """
        fb = RetrievalFeedback(
            id=str(uuid.uuid4()),
            trace_id=trace_id,
            score=score,
            notes=notes
        )
        db.add(fb)
        await db.commit()
        return fb
