# Collaborative Handoff Protocol

Strict schema validation gating transitions between collaborating specialists.

## 1. Authorized Handoff Sequence
To prevent uncontrolled cyclic chatter loops, handoffs must match registered transitions:
- `CodeReviewerAgent` -> `DatabaseAuditorAgent`
- `DatabaseAuditorAgent` -> `WorkflowDiagnosticianAgent`
- `WorkflowDiagnosticianAgent` -> `SafetyPolicyCheckerAgent`

## 2. Handoff Contracts
- Payloads are checked by `CollaborationContractValidator` to guarantee necessary parameters are present before the receiving agent processes it.
