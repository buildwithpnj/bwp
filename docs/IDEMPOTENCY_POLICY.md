# Idempotency Guard & Duplication Policy

The execution engine protects system integrity and prevents duplicate state pollution using deterministic idempotency controls.

## Enforcement Mechanism

Every request is assigned a unique `idempotency_key` calculated as the SHA-256 hash of:
```python
sha256( f"{user_id}:{action_name}:{sorted_json_payload}" )
```

Before execution, the `IdempotencyGuard` queries history:
1. **New Request**: Key not found. Cleared to execute.
2. **Success (Duplicate)**: An action log with this key already has `execution_status = succeeded`. The request is **blocked** and returns `DuplicateRequestException` to prevent duplicate writes.
3. **In-Progress**: An action log with this key is currently `executing` or `queued`. The request is **blocked** to prevent race conditions.
4. **Retry of Failed Run**: An action log with this key exists with a state of `failed`. The request is passed through only if the retry policy permits.

## Idempotency Key Configuration
Enforced at the backend orchestrator boundary (`ActionExecutionService.request_execution`) ensuring safety across all clients.
