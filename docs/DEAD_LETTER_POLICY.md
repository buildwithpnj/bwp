# Dead Letter Queue (DLQ) Policy

Handles unrecoverable execution crashes and administrative replays.

## Quarantine Criteria
Jobs are moved to DLQ only if:
1. Max retries are exceeded (3 for practices, 2 for lesson notes).
2. A non-retryable action (like preference writes) encounters an execution exception.
3. Database constraints are violated during intermediate writes.

## Admin Replay Endpoint
- Exposed under `POST /api/actions/admin/dlq/replay/{log_id}` (Restricted to `internal_admin`).
- Resets retry count to `0` and enqueues job into `MemoryQueueAdapter`.
