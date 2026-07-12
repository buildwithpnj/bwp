import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.agent_memory_context_builder import AgentMemoryContextBuilder
from app.models.user_profile_memory import UserProfileMemory
from app.models.learning_progress import LearningProgress

@pytest.mark.asyncio
async def test_build_memory_context_block():
    db = AsyncMock()
    
    # Mock user profile and learning progress fetches
    profile = UserProfileMemory(user_id="user_123", tone="concise", explanation_style="brief", weaknesses=["articles"])
    progress = LearningProgress(
        user_id="user_123", 
        streak=5, 
        corrections_accepted=10, 
        weak_categories=["prepositions"],
        mastered_patterns=[]
    )
    
    mock_prof_res = MagicMock()
    mock_prof_res.scalar_one_or_none.return_value = profile
    
    mock_prog_res = MagicMock()
    mock_prog_res.scalar_one_or_none.return_value = progress
    
    db.execute.side_effect = [mock_prof_res, mock_prog_res]
    
    block = await AgentMemoryContextBuilder.build_context_block(db, "user_123")
    assert "USER PERSONALIZATION PROFILE" in block
    assert "USER LEARNING PROGRESS" in block
    assert "concise" in block
    assert "Streak" in block
