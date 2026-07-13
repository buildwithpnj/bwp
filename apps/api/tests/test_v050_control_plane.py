import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.action_execution_service import ActionExecutionService
from app.models.action_models import ActionLog

async def run_action(action_name: str, payload: dict) -> dict:
    db = AsyncMock()
    # Mock database responses for all model types
    mock_result = MagicMock()
    mock_item = MagicMock()
    mock_item.id = "dummy-id"
    mock_item.title = "Dummy Title"
    mock_item.name = "Dummy Name"
    mock_item.user_id = "user_123"
    mock_item.pinned = False
    mock_item.status = "active"
    mock_item.body_json = {}
    mock_item.tags = []
    mock_item.item_id = "dummy-id"
    mock_item.item_type = "note"
    mock_item.original_data = {"title": "Dummy", "body_json": {}, "tags": [], "name": "Dummy", "author": "Author", "cadence": "daily", "target": 1}
    mock_item.goals = ["fact"]
    
    mock_result.scalar_one_or_none.return_value = mock_item
    mock_result.scalars.return_value.all.return_value = [mock_item]
    db.execute.return_value = mock_result
    
    log = ActionLog(
        id="test-log-id",
        user_id="user_123",
        action_name=action_name,
        input_payload=payload,
        status="pending"
    )
    return await ActionExecutionService.execute_log_action(db, log)

@pytest.mark.asyncio
async def test_action_01_create_note():
    res = await run_action("create_note", {"title": "Test Title", "content": "Test Body"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_02_update_note():
    res = await run_action("update_note", {"note_id": "note_123", "title": "New Title", "content": "New Content"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_03_delete_note():
    res = await run_action("delete_note", {"note_id": "note_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_04_restore_note():
    res = await run_action("restore_note", {"note_id": "note_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_05_search_notes():
    res = await run_action("search_notes", {"query": "hello"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_06_create_task():
    res = await run_action("create_task", {"title": "Test Task", "description": "Desc"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_07_update_task():
    res = await run_action("update_task", {"task_id": "task_123", "status": "completed"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_08_complete_task():
    res = await run_action("complete_task", {"task_id": "task_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_09_prioritize_task():
    res = await run_action("prioritize_task", {"task_id": "task_123", "pinned": True})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_10_delete_task():
    res = await run_action("delete_task", {"task_id": "task_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_11_restore_task():
    res = await run_action("restore_task", {"task_id": "task_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_12_create_project():
    res = await run_action("create_project", {"name": "Test Project", "description": "Desc"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_13_update_project():
    res = await run_action("update_project", {"project_id": "proj_123", "status": "completed"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_14_complete_project():
    res = await run_action("complete_project", {"project_id": "proj_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_15_delete_project():
    res = await run_action("delete_project", {"project_id": "proj_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_16_create_book():
    res = await run_action("create_book", {"title": "Test Book", "author": "Author"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_17_update_book_progress():
    res = await run_action("update_book_progress", {"book_id": "book_123", "status": "finished", "rating": 5})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_18_archive_book():
    res = await run_action("archive_book", {"book_id": "book_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_19_delete_book():
    res = await run_action("delete_book", {"book_id": "book_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_20_create_asset():
    res = await run_action("create_asset", {"name": "Asset 1", "provider": "s3", "bucket": "b1"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_21_update_asset():
    res = await run_action("update_asset", {"asset_id": "asset_123", "name": "New Asset"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_22_delete_asset():
    res = await run_action("delete_asset", {"asset_id": "asset_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_23_upload_media_metadata():
    res = await run_action("upload_media_metadata", {"title": "Media 1", "file_path": "/path"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_24_update_media_metadata():
    res = await run_action("update_media_metadata", {"media_id": "media_123", "title": "New Title"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_25_delete_media_metadata():
    res = await run_action("delete_media_metadata", {"media_id": "media_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_26_get_storage_status():
    res = await run_action("get_storage_status", {})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_27_cleanup_storage():
    res = await run_action("cleanup_storage", {"days_old": 30})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_28_create_calendar_event():
    res = await run_action("create_calendar_event", {"title": "Meeting", "start_time": "2026-07-14T10:00:00", "end_time": "2026-07-14T11:00:00"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_29_update_calendar_event():
    res = await run_action("update_calendar_event", {"event_id": "evt_123", "title": "New Meeting"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_30_cancel_calendar_event():
    res = await run_action("cancel_calendar_event", {"event_id": "evt_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_31_create_habit():
    res = await run_action("create_habit", {"name": "Yoga", "cadence": "daily", "target": 1})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_32_log_habit_checkin():
    res = await run_action("log_habit_checkin", {"habit_id": "habit_123", "date": "2026-07-14", "value": 1.0})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_33_delete_habit():
    res = await run_action("delete_habit", {"habit_id": "habit_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_34_create_addiction_tracker():
    res = await run_action("create_addiction_tracker", {"name": "Sugar", "quit_date": "2026-07-01T00:00:00"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_35_log_addiction_relapse():
    res = await run_action("log_addiction_relapse", {"tracker_id": "track_123", "relapse_date": "2026-07-14T00:00:00"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_36_get_sobriety_stats():
    res = await run_action("get_sobriety_stats", {"tracker_id": "track_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_37_create_memory_item():
    res = await run_action("create_memory_item", {"fact": "User likes dark theme", "category": "preference"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_38_update_memory_item():
    res = await run_action("update_memory_item", {"tone": "formal", "explanation_style": "simple"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_39_delete_memory_item():
    res = await run_action("delete_memory_item", {"fact": "fact"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_40_create_knowledge_item():
    res = await run_action("create_knowledge_item", {"title": "AI Platform", "content": "Knowledge content"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_41_search_knowledge():
    res = await run_action("search_knowledge", {"query": "AI"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_42_delete_knowledge_item():
    res = await run_action("delete_knowledge_item", {"item_id": "item_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_43_get_telemetry_status():
    res = await run_action("get_telemetry_status", {})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_44_trigger_system_sync():
    res = await run_action("trigger_system_sync", {})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_45_update_preference():
    res = await run_action("update_preference", {"tone": "casual", "explanation_style": "simple"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_46_update_reminder_preferences():
    res = await run_action("update_reminder_preferences", {"frequency": "daily"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_47_list_trash_items():
    res = await run_action("list_trash_items", {})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_48_restore_trash_item():
    res = await run_action("restore_trash_item", {"item_type": "note", "item_id": "note_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_49_permanent_purge_item():
    res = await run_action("permanent_purge_item", {"item_type": "note", "item_id": "note_123"})
    assert res["status"] == "success"

@pytest.mark.asyncio
async def test_action_50_invalid_action_payload_validation():
    # Enforce schema validation error through registry directly
    from app.services.copilot_action_registry import CopilotActionRegistry
    is_valid = CopilotActionRegistry.validate_inputs("create_note", {"content_wrong": "only"})
    assert is_valid is False
