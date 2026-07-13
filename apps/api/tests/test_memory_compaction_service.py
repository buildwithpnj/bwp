import pytest
from unittest.mock import AsyncMock
from app.services.memory_compaction_service import MemoryCompactionService
from app.services.context_budget_manager import ContextBudgetManager

@pytest.mark.asyncio
async def test_memory_compaction_ratios():
    db = AsyncMock()
    
    traces = [
        {"id": "wf_1", "status": "succeeded", "steps": [{}, {}]},
        {"id": "wf_2", "status": "failed", "steps": [{}]}
    ]
    
    # 1. Compact context
    compacted = await MemoryCompactionService.compact_memory(db, "usr_123", traces)
    assert "Run wf_1" in compacted
    assert "Run wf_2" in compacted
    
    # 2. Token budget check
    assert ContextBudgetManager.check_context_overload(1500) is False
    assert ContextBudgetManager.check_context_overload(5000) is True
