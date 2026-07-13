import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.chunking_strategy_service import ChunkingStrategyService

class HybridIndexCoordinator:
    @classmethod
    async def index_document_chunks(
        cls,
        db: AsyncSession,
        document_id: str,
        tenant_id: str,
        text: str
    ) -> int:
        """
        Segments text and stores generated knowledge chunks in DB.
        """
        chunks = ChunkingStrategyService.segment_document(text)
        created_count = 0
        
        for item in chunks:
            chunk = KnowledgeChunk(
                id=str(uuid.uuid4()),
                document_id=document_id,
                tenant_id=tenant_id,
                chunk_text=item["text"],
                chunk_summary=f"Summary of {item['heading']}",
                token_count=len(item["text"].split()),
                heading_hierarchy=item["heading"]
            )
            db.add(chunk)
            created_count += 1
            
        await db.commit()
        return created_count
