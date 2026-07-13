# Observability & Administrative Auditing

Telemetry outputs structured logs, latency tracking, and timeline traces for internal monitoring.

## 1. Machine-Readable Log Events

JSON line outputs emitted under `action_observability` logger:
```json
{"timestamp": "2026-07-13T07:42:00.123456Z", "event": "action_succeeded", "user_id": "user_123", "action_name": "create_lesson_note", "action_log_id": "log_123", "latency_ms": 142.5}
```

## 2. Admin Metrics API Endpoint
Exposed under `GET /api/actions/metrics` (Admin/internal_admin role only):
- Aggregates suggestion counts, accept/reject approval rates, latency averages, failure reasons, and duplicate blocks.

## 3. Human-Readable Lifecycle Debug Traces
Exposed under `GET /api/actions/admin/trace/{log_id}` (Admin only) returns formatted timeline view:
```text
=== Action Execution Trace: create_lesson_note ===
Log ID: log_123
User ID: user_123
Idempotency Key: 62d...
Status: SUCCEEDED (Recovery: NONE)
Timeline:
  + 0.000s | Suggested At (2026-07-13T07:42:00.000Z)
  + 0.005s | Approved At (2026-07-13T07:42:00.005Z)
  + 0.010s | Execution Started At (2026-07-13T07:42:00.010Z)
  + 0.152s | Executed/Succeeded At (2026-07-13T07:42:00.152s)
```
Used by developers to debug slow steps or locate transaction bottlenecks.
