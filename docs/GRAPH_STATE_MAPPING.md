# Graph State Mapping Rules

Maps backend execution and recovery statuses into graph visualization properties.

## State Mapping Table

| Backend State | Node Status | Badges & Annotations |
|---|---|---|
| `pending` | `pending` | Neutral gray outline |
| `executing` | `executing` | Pulsing blue border, progress loader |
| `paused_approval` | `paused` | Yellow badge "Awaiting Checkpoint Approval" |
| `succeeded` | `succeeded` | Solid green, checkmark icon |
| `failed` | `failed` | Solid red, click indicator |
| `cancelled` | `cancelled` | Striped gray, rollback arrow markers |
