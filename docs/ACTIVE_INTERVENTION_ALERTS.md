# Active Intervention Alerts & Actionable Notifications

Describes the notification feed engine logging alert events and dispatch rules.

## 1. Dispatching & Priority
- Evaluates event source classifications to assign priority (e.g. `workflow_failure` yields `high` priority).
- Delivery is logged across channel limits (e.g. `in_app`).

## 2. Sliding Window Deduplication
- Suppresses repeated identical warnings or alert payloads within 60s windows to avoid notification spam.

## 3. Direct Actions routing
- Supports structural commands (approve/pause/resume/cancel) directly from the action bar.
