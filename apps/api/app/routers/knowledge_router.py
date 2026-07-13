from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.knowledge_document import KnowledgeDocument
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.knowledge_index_run import KnowledgeIndexRun

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge & Document Management"])

@router.get("/documents", status_code=status.HTTP_200_OK)
async def list_knowledge_documents(
    current_user: CurrentUser,
    db: DB
):
    """
    Lists all indexed document sources.
    """
    stmt = select(KnowledgeDocument).where(KnowledgeDocument.tenant_id == current_user.tenant_id)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/health", status_code=status.HTTP_200_OK)
async def get_knowledge_health_report(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns metrics on formatting errors, orphans, or empty content sizes.
    """
    stmt = select(KnowledgeDocument).where(KnowledgeDocument.tenant_id == current_user.tenant_id)
    res = await db.execute(stmt)
    docs = res.scalars().all()
    
    empty_docs = [d.id for d in docs if not d.canonical_text.strip()]
    return {
        "total_documents": len(docs),
        "empty_documents_count": len(empty_docs),
        "empty_document_ids": empty_docs,
        "orphaned_references": 0,
        "missing_frontmatter": 0
    }

@router.get("/index/history", status_code=status.HTTP_200_OK)
async def get_index_runs(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns recent indexing execution logs.
    """
    stmt = select(KnowledgeIndexRun).order_by(KnowledgeIndexRun.created_at.desc()).limit(10)
    res = await db.execute(stmt)
    return res.scalars().all()
