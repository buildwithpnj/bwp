import pytest
import asyncio
from app.services.preview_timeout_handler import PreviewTimeoutHandler

@pytest.mark.asyncio
async def test_execution_timeout_trigger(monkeypatch):
    monkeypatch.setattr(PreviewTimeoutHandler, "TIMEOUT_LIMIT", 0.1)
    async def slow_function():
        await asyncio.sleep(0.2)  # Exceeds the 0.1 seconds limit
        return "done"

    with pytest.raises(TimeoutError):
        await PreviewTimeoutHandler.execute_with_timeout(slow_function)
