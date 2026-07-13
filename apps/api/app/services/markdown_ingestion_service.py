import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge_document import KnowledgeDocument
from app.services.frontmatter_parser import FrontmatterParser
from app.services.knowledge_hash_service import KnowledgeHashService
from app.services.document_cleaning_service import DocumentCleaningService

class MarkdownIngestionService:
    @classmethod
    async def ingest_file(
        cls,
        db: AsyncSession,
        file_path: str,
        tenant_id: str
    ) -> KnowledgeDocument:
        """
        Parses frontmatter metadata, cleans normal text, and stores document in database.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
            
        metadata, body = FrontmatterParser.parse_content(raw_content)
        cleaned_body = DocumentCleaningService.clean_text(body)
        content_hash = KnowledgeHashService.compute_hash(cleaned_body)
        
        doc = KnowledgeDocument(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            source_type="markdown",
            source_path=file_path,
            title=metadata.get("title", os.path.basename(file_path)),
            slug=metadata.get("slug", os.path.basename(file_path).replace(".md", "")),
            content_hash=content_hash,
            canonical_text=cleaned_body,
            visibility_scope=metadata.get("visibility", "internal")
        )
        db.add(doc)
        await db.commit()
        return doc
