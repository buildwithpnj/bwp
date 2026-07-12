import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.learning_progress_service import LearningProgressService
from app.models.learning_progress import LearningProgress

@pytest.mark.asyncio
async def test_record_correction_progress():
    db = AsyncMock()
    
    # Mock progress existence
    progress = LearningProgress(user_id="user_123", corrections_accepted=5, streak=3, mastered_patterns=[])
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = progress
    db.execute.return_value = mock_res
    
    updated = await LearningProgressService.record_correction(db, "user_123", "nouns", was_correct=True)
    assert updated.corrections_accepted == 6
    assert updated.streak == 4
    assert "nouns" in updated.mastered_patterns
    db.commit.assert_called_once()
