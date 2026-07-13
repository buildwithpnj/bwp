# Human Intervention Audit Model

Audits and metrics logged for every control-plane intervention.

## 1. Audit Trail Record
Interventions are logged in the `workflow_control_events` table:
- Who requested the control (`requested_by_user_id`, `requested_by_role`)
- What action was taken (`control_type`, `applied_at`)
- The reasoning/justification (`reason`)
- Outcome result status (`result_status`)

## 2. Operational Metrics
- Exposes `GET /api/workflows/admin/controls/audit` (Admin only) aggregating total counts by status and control type to analyze intervention frequency.
