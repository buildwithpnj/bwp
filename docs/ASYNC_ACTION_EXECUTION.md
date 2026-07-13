# Asynchronous Action Execution

This document details the background queue structure and job execution pathways.

## Architecture Diagram

```mermaid
sequenceDiagram
    participant User/API
    participant ActionExecutionService
    participant QueueAdapter (Memory)
    participant ActionWorker
    participant Executor

    User/API->>ActionExecutionService: request_execution()
    Note over ActionExecutionService: Check gates & validators
    ActionExecutionService->>QueueAdapter: enqueue(job)
    ActionExecutionService-->>User/API: Return status="queued", job_id
    
    loop Worker Poll
        ActionWorker->>QueueAdapter: dequeue()
        QueueAdapter-->>ActionWorker: return job
        Note over ActionWorker: Validate log status
        Note over ActionWorker: Re-check idempotency key
        ActionWorker->>Executor: execute()
        Executor-->>ActionWorker: Success / Failure
        Note over ActionWorker: Update timestamps & logs
    end
```

## Active Queue Adapters
- `MemoryQueueAdapter`: Wraps `asyncio.Queue` for sandboxed, database-mocked, thread-safe asynchronous local execution.
