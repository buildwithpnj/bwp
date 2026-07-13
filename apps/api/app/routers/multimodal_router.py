from fastapi import APIRouter, status
from app.deps import CurrentUser, DB
from app.schemas.multimodal_input_schema import MultimodalInput
from app.services.multimodal_ingestion_service import MultimodalIngestionService

router = APIRouter(prefix="/api/multimodal", tags=["Multimodal Ingestion Pipeline"])

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_multimodal_signal(
    req: MultimodalInput,
    current_user: CurrentUser,
    db: DB
):
    """
    Submits a raw media attachment (text, screenshot, voice transcript, pdf)
    to normalize contents, run safety screening, and route workflow action tasks.
    """
    res = await MultimodalIngestionService.ingest_media(db, req)
    return res
