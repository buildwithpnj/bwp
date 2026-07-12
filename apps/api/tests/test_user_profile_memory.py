import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_profile_memory_service import UserProfileMemoryService
from app.models.user_profile_memory import UserProfileMemory

@pytest.mark.asyncio
async def test_get_or_create_user_profile():
    db = AsyncMock()
    
    # Mock return value to None first (trigger creation flow)
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_res
    
    async def mock_refresh(obj):
        obj.id = "prof_123"
    db.refresh = mock_refresh
    
    profile = await UserProfileMemoryService.get_or_create_profile(db, "user_123")
    assert profile.user_id == "user_123"
    assert profile.tone == "professional"
    db.add.assert_called_once()
    db.commit.assert_called_once()
