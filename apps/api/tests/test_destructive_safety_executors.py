import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.actions.v050_executors import (
    DeleteNoteAction,
    RestoreNoteAction,
    DeleteTaskAction,
    RestoreTaskAction,
    RestoreTrashItemAction,
    PermanentPurgeItemAction
)
from app.models.notes import Note
from app.models.goals import Goal
from app.models.action_models import TrashItem

@pytest.mark.asyncio
async def test_delete_note_soft_deletes_to_trash():
    db = AsyncMock()
    user_id = "user_123"
    note_id = "note_123"
    
    note = Note(id=note_id, user_id=user_id, title="Test Note", body_json="{}", tags="test")
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = note
    db.execute.return_value = mock_res
    
    res = await DeleteNoteAction.execute(db, user_id, {"note_id": note_id})
    
    assert res["status"] == "success"
    assert "moved to trash" in res["message"]
    
    # Verify the note is deleted and trash item is added
    db.delete.assert_called_once_with(note)
    db.add.assert_called_once()
    trash_arg = db.add.call_args[0][0]
    assert isinstance(trash_arg, TrashItem)
    assert trash_arg.item_id == note_id
    assert trash_arg.item_type == "note"
    assert trash_arg.original_data["title"] == "Test Note"

@pytest.mark.asyncio
async def test_restore_note_recreates_note():
    db = AsyncMock()
    user_id = "user_123"
    note_id = "note_123"
    
    trash = TrashItem(
        id="trash_123",
        user_id=user_id,
        item_type="note",
        item_id=note_id,
        original_data={"title": "Test Note", "body_json": "{}", "tags": "test"}
    )
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = trash
    db.execute.return_value = mock_res
    
    res = await RestoreNoteAction.execute(db, user_id, {"note_id": note_id})
    
    assert res["status"] == "success"
    assert "restored successfully" in res["message"]
    
    db.delete.assert_called_once_with(trash)
    # Check that Note was added back
    assert db.add.call_count == 1
    note_arg = db.add.call_args[0][0]
    assert isinstance(note_arg, Note)
    assert note_arg.id == note_id
    assert note_arg.title == "Test Note"

@pytest.mark.asyncio
async def test_delete_task_soft_deletes_to_trash():
    db = AsyncMock()
    user_id = "user_123"
    task_id = "task_123"
    
    task = Goal(id=task_id, user_id=user_id, title="Test Task", status="pending", progress=0)
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = task
    db.execute.return_value = mock_res
    
    res = await DeleteTaskAction.execute(db, user_id, {"task_id": task_id})
    
    assert res["status"] == "success"
    assert "moved to trash" in res["message"]
    
    db.delete.assert_called_once_with(task)
    db.add.assert_called_once()
    trash_arg = db.add.call_args[0][0]
    assert isinstance(trash_arg, TrashItem)
    assert trash_arg.item_id == task_id
    assert trash_arg.item_type == "task"
    assert trash_arg.original_data["title"] == "Test Task"

@pytest.mark.asyncio
async def test_restore_task_recreates_task():
    db = AsyncMock()
    user_id = "user_123"
    task_id = "task_123"
    
    trash = TrashItem(
        id="trash_456",
        user_id=user_id,
        item_type="task",
        item_id=task_id,
        original_data={"title": "Test Task", "status": "pending", "progress": 10}
    )
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = trash
    db.execute.return_value = mock_res
    
    res = await RestoreTaskAction.execute(db, user_id, {"task_id": task_id})
    
    assert res["status"] == "success"
    assert "restored successfully" in res["message"]
    
    db.delete.assert_called_once_with(trash)
    assert db.add.call_count == 1
    task_arg = db.add.call_args[0][0]
    assert isinstance(task_arg, Goal)
    assert task_arg.id == task_id
    assert task_arg.title == "Test Task"

@pytest.mark.asyncio
async def test_permanent_purge_deletes_trash_item():
    db = AsyncMock()
    user_id = "user_123"
    item_id = "note_123"
    
    trash = TrashItem(id="trash_123", user_id=user_id, item_type="note", item_id=item_id)
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = trash
    db.execute.return_value = mock_res
    
    res = await PermanentPurgeItemAction.execute(db, user_id, {"item_type": "note", "item_id": item_id})
    
    assert res["status"] == "success"
    assert "permanently purged" in res["message"]
    db.delete.assert_called_once_with(trash)
