import pytest
from unittest.mock import AsyncMock
from app.services.operating_thread_service import OperatingThreadService
from app.schemas.operating_thread_schema import OperatingThreadCreate
from app.services.thread_context_assembler import ThreadContextAssembler
from app.services.thread_transition_service import ThreadTransitionService

@pytest.mark.asyncio
async def test_operating_threads_continuity():
    db = AsyncMock()
    
    # 1. Create continuity thread
    data = OperatingThreadCreate(title="Investigating quota", description="Investigating upload errors")
    thread = await OperatingThreadService.create_thread(db, "usr_123", data)
    
    assert thread.title == "Investigating quota"
    assert thread.status == "active"
    
    # 2. Link context
    link = await ThreadContextAssembler.link_entity_to_thread(db, thread.id, "workflow_run", "wf_run_99")
    assert link.linked_entity_id == "wf_run_99"
    
    # 3. Transition state
    updated = await ThreadTransitionService.transition_thread(db, thread, "paused")
    assert updated.status == "paused"
