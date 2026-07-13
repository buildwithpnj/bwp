# Policy Explainability

Ensures all adaptive policy shifts remain explainable and auditable.

## 1. Auditable Logging
- Adaptive changes are driven directly from the `delegation_policy_feedbacks` table.
- Explainability logs record usefulness averages and total feedback count, giving admins transparent insight into why a specific specialist was blocked on a workflow type.
- Rollback actions are audited.
