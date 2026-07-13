import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.project_action_service import ProjectActionService
from app.models.project_item import ProjectItem

@pytest.mark.asyncio
async def test_create_project_item_success():
    db = AsyncMock()
    
    project = await ProjectActionService.create_project_item(
        db=db,
        user_id="user_777",
        name="warborn launch polish",
        description="Verify V0.50 release checklist"
    )
    
    assert project.user_id == "user_777"
    assert project.name == "warborn launch polish"
    assert project.status == "active"
    assert db.add.called
    assert db.commit.called

@pytest.mark.asyncio
async def test_update_project_item_status():
    db = AsyncMock()
    existing_project = ProjectItem(
        user_id="user_777",
        name="warborn launch polish",
        status="active"
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = existing_project
    db.execute.return_value = mock_res
    
    updated = await ProjectActionService.update_project_item_status(db, "project_abc", "completed")
    assert updated.status == "completed"
