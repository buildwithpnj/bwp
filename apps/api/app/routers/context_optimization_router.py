from fastapi import APIRouter, status
from typing import List, Dict, Any
from app.deps import CurrentUser, DB
from app.services.memory_compaction_service import MemoryCompactionService

router = APIRouter(prefix="/api/context", tags=["Knowledge & Context Optimization"])

@router.post("/compact", status_code=status.HTTP_200_OK)
async def trigger_context_compaction(
    raw_traces: List[Dict[str, Any]],
    current_user: CurrentUser,
    db: DB
):
    """
    Compacts historical workflow traces to optimize downstream context budgets and latency.
    """
    compacted = await MemoryCompactionService.compact_memory(db, current_user.id, raw_traces)
    return {
        "compacted_summary": compacted,
        "status": "compacted"
    }
