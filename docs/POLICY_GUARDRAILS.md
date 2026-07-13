# Adaptive Policy Safety Guardrails

Guards policy adjustments and outlines recovery rollbacks.

## 1. Shift Magnitude Caps
- Threshold shifts are validated by `PolicyChangeGuard`. Maximum allowed change in a single adaptation is `0.5`.
- Larger swings are blocked, requiring manual override.

## 2. Policy Rollback
- Administrative endpoint `POST /api/delegation/policy/rollback` allows instantly clearing historical feedback to restore baseline defaults.
