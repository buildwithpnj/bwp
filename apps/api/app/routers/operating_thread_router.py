from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.deps import CurrentUser, DB
from app.models.operating_thread import OperatingThread
from app.schemas.operating_thread_schema import OperatingThreadCreate
from app.services.operating_thread_service import OperatingThreadService
from app.services.thread_context_assembler import ThreadContextAssembler
from app.services.thread_transition_service import ThreadTransitionService

router = APIRouter(prefix="/api/threads", tags=["Cross-Page Continuity Threads"])

@router.get("/list", status_code=status.HTTP_200_OK)
async def list_operating_threads(
    current_user: CurrentUser,
    db: DB
):
    """
    Returns active operating threads for maintaining task focus across routes.
    """
    stmt = select(OperatingThread).where(
        OperatingThread.user_id == current_user.id
    ).order_by(OperatingThread.updated_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_operating_thread(
    data: OperatingThreadCreate,
    current_user: CurrentUser,
    db: DB
):
    """
    Creates a new user operating thread.
    """
    return await OperatingThreadService.create_thread(db, current_user.id, data)

@router.post("/{thread_id}/transition", status_code=status.HTTP_200_OK)
async def transition_thread_status(
    thread_id: str,
    new_status: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Updates active thread status (active, paused, archived).
    """
    stmt = select(OperatingThread).where(
        OperatingThread.id == thread_id,
        OperatingThread.user_id == current_user.id
    )
    res = await db.execute(stmt)
    thread = res.scalar_one_or_none()
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found."
        )
        
    return await ThreadTransitionService.transition_thread(db, thread, new_status)

@router.post("/{thread_id}/link", status_code=status.HTTP_201_CREATED)
async def link_entity_to_thread(
    thread_id: str,
    entity_type: str,
    entity_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Links a workflow run or objective to this operating thread.
    """
    # Verify thread exists
    stmt = select(OperatingThread).where(
        OperatingThread.id == thread_id,
        OperatingThread.user_id == current_user.id
    )
    res = await db.execute(stmt)
    thread = res.scalar_one_or_none()
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found."
        )
        
    return await ThreadContextAssembler.link_entity_to_thread(db, thread_id, entity_type, entity_id)
