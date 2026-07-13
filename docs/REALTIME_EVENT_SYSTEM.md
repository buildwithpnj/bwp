# Real-Time Event System

Exposes a streaming push interface for clients to monitor action and workflow runs.

## 1. Event schema
All WebSocket push frames match the following structure:
```json
{
  "event_id": "8a68846c-c9e2-4148-932d-eb3b2e557ff2",
  "event_type": "workflow.step_started",
  "occurred_at": "2026-07-13T08:35:00.123456Z",
  "user_id": "user_123",
  "workflow_run_id": "wf_abc",
  "summary_message": "Starting workflow step: create_lesson_note",
  "safe_metadata": {"step_index": 1}
}
```

## 2. Event Types reference
- `action.suggested` / `action.queued` / `action.executing` / `action.succeeded` / `action.failed`
- `workflow.started` / `workflow.step_started` / `workflow.step_succeeded` / `workflow.step_failed` / `workflow.paused_for_approval` / `workflow.completed` / `workflow.cancelled`
- `workflow.paused` / `workflow.resumed`
