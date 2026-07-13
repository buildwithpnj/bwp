from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.knowledge_document import KnowledgeDocument

class KnowledgeChangeDetector:
    @classmethod
    async def has_changed(
        cls,
        db: AsyncSession,
        source_path: str,
        current_hash: str
    ) -> bool:
        """
        Detects if content hash has changed compared to database records.
        """
        stmt = select(KnowledgeDocument).where(KnowledgeDocument.source_path == source_path)
        res = await db.execute(stmt)
        existing = res.scalar_one_or_none()
        if not existing:
            return True
        return existing.content_hash != current_hash
