# Worker Lifecycle & State Transitions

Details of task states from initial suggestion to final completion inside the task queues.

## Lifecycle Transitions
- **`suggested`**: Request registered.
- **`pending_approval`**: Held at gate waiting for user decision.
- **`queued`**: Pushed onto processing queue.
- **`executing`**: Pulled by worker.
- **`succeeded`**: Executor returned successfully.
- **`failed`**: Executor crashed. Schedules retry or DLQ move.
- **`permanently_failed`**: Max retries exceeded. Rollback triggered.

## Recovery Scan Policy
- `RecoveryWorker` scans items stuck in `queued` or `executing` states for >5 minutes.
- Stale jobs are re-queued if `retry_count < max_retries`, or moved to `permanently_failed` if exhausted.
