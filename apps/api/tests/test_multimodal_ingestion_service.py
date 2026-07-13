import pytest
from unittest.mock import AsyncMock
from app.services.multimodal_ingestion_service import MultimodalIngestionService
from app.schemas.multimodal_input_schema import MultimodalInput

@pytest.mark.asyncio
async def test_multimodal_ingestion_safety_and_routing():
    db = AsyncMock()
    
    # 1. Normal safe document ingestion
    req = MultimodalInput(
        media_type="document",
        raw_filename="lesson_note.pdf",
        file_bytes=b"Learn Spanish grammar lessons."
    )
    
    res = await MultimodalIngestionService.ingest_media(db, req)
    assert res["status"] == "success"
    assert res["workflow_proposal"]["suggested_workflow_type"] == "create_lesson_note"
    assert db.commit.call_count > 0
    
    # 2. Malicious payload ingestion (intercepted by safety guard)
    req_unsafe = MultimodalInput(
        media_type="text",
        raw_filename="hack.txt",
        file_bytes=b"DROP TABLE users;"
    )
    
    res_unsafe = await MultimodalIngestionService.ingest_media(db, req_unsafe)
    assert res_unsafe["status"] == "blocked"
    assert "Security policy violation" in res_unsafe["message"]
