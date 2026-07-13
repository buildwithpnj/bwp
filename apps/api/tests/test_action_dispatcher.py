import pytest
from app.services.action_dispatcher import ActionDispatcher
from app.services.queue_adapter import MemoryQueueAdapter, QueueJob

@pytest.mark.asyncio
async def test_action_dispatcher_enqueue_dequeue():
    # Setup memory adapter
    adapter = MemoryQueueAdapter()
    await adapter.clear("actions")
    ActionDispatcher.set_adapter(adapter)

    job_id = await ActionDispatcher.dispatch(
        action_log_id="log_123",
        action_name="create_lesson_note",
        user_id="user_123",
        metadata={"queue_name": "actions"}
    )
    
    assert job_id is not None
    assert await adapter.size("actions") == 1
    
    # Dequeue
    job = await adapter.dequeue("actions")
    assert job is not None
    assert job.job_id == job_id
    assert job.action_log_id == "log_123"
    assert job.action_name == "create_lesson_note"
    assert job.user_id == "user_123"
    
    assert await adapter.size("actions") == 0
