import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.retrieval_trace import RetrievalTrace

class RetrievalObservabilityService:
    @classmethod
    async def log_trace(
        cls,
        db: AsyncSession,
        query: str,
        rewritten: str,
        strategy: str,
        latency: float,
        confidence: float
    ) -> RetrievalTrace:
        """
        Stores structured trace latency parameters.
        """
        trace = RetrievalTrace(
            id=str(uuid.uuid4()),
            query_text=query,
            rewritten_query=rewritten,
            strategy_used=strategy,
            latency_ms=latency,
            confidence_score=confidence
        )
        db.add(trace)
        await db.commit()
        return trace
