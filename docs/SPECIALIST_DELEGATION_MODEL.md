# Policy-Aware Specialist Delegation Model

Describes specialist subagent triggers, input domains, and validation.

## 1. Specialist Purpose
Specialists function strictly in advisory capacities. They cannot write directly to application DB tables or execute operations.

## 2. Delegation request & response
Delegations must conform to:
- `DelegationRequest`: ID, goal, context, allowed tools, and timeout bounds.
- `DelegationResponse`: Reasoning summary, structured findings, suggested next step, and confidence score.
