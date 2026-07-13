import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.memory_action_service import MemoryActionService
from app.models.user_profile_memory import UserProfileMemory

@pytest.mark.asyncio
async def test_create_memory_item_success():
    db = AsyncMock()
    profile = UserProfileMemory(
        user_id="user_999",
        goals=["existing fact"]
    )
    
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = profile
    db.execute.return_value = mock_res
    
    updated_profile = await MemoryActionService.create_memory_item(
        db=db,
        user_id="user_999",
        fact="deep focus work mode preferred"
    )
    
    assert "deep focus work mode preferred" in updated_profile.goals
    assert db.add.called
    assert db.commit.called
