import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.objective_manager import ObjectiveManager
from app.schemas.objective_schema import ObjectiveCreate
from app.services.objective_progress_service import ObjectiveProgressService
from app.services.objective_review_service import ObjectiveReviewService

@pytest.mark.asyncio
async def test_objectives_lifecycle_and_checkpoints():
    db = AsyncMock()
    
    # 1. Create goal
    data = ObjectiveCreate(title="Complete math study", description="Study daily", stop_condition="verified progress")
    obj = await ObjectiveManager.create_objective(db, "usr_xyz", data)
    
    assert obj.title == "Complete math study"
    assert obj.progress_percent == 0.0
    
    # 2. Checkpoint review
    mock_res = MagicMock()
    cp = MagicMock()
    cp.status = "pending"
    mock_res.scalar_one_or_none.return_value = cp
    db.execute.return_value = mock_res
    
    verified = await ObjectiveReviewService.evaluate_checkpoint(db, "cp_1", "checkpoint study successful")
    assert verified is True
    
    # Mock progress calculation count queries
    mock_count = MagicMock()
    mock_count.scalar.side_effect = [1, 1]  # total = 1, verified = 1
    db.execute.return_value = mock_count
    
    # Update progress
    progress = await ObjectiveProgressService.update_objective_progress(db, obj.id)
    assert progress == 100.0
