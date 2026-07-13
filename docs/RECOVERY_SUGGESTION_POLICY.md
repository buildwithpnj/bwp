# Recovery Suggestion & Safety Policy

Assigns risk evaluations to ensure safety gates are never bypassed during recovery proposals.

## 1. Safety Gates
- Standard recovery operations (`replay_failed_step`, `cancel_workflow`) require standard user approval.
- High-severity operations (`escalate_to_admin`) are marked `admin_only=True` to prevent standard users from overriding systems boundaries.

## 2. Risk Scoring reference
- `replay_failed_step`: 0.1
- `cancel_workflow`: 0.3
- `switch_to_alternate`: 0.5
- `escalate_to_admin`: 0.8
- Safe suggestions are sorted by risk score ascending (safest option first).
