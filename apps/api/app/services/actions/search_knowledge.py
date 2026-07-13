from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.knowledge_document import KnowledgeDocument

class SearchKnowledgeAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = payload["query"]
        
        # Simple text query across document metadata
        stmt = select(KnowledgeDocument).where(KnowledgeDocument.title.ilike(f"%{query}%")).limit(5)
        res = await db.execute(stmt)
        docs = res.scalars().all()
        
        doc_titles = [doc.title for doc in docs]
        return {
            "status": "success",
            "message": f"Knowledge base search complete. Found {len(docs)} documents.",
            "results": doc_titles
        }
