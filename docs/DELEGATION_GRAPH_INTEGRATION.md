# Delegation Graph Integration

Visual step graph representations of specialist delegation runs.

## 1. Graph representation
- Delegated runs are appended as subnodes: `node_{workflow_run_id}_specialist_{delegation_id}`.
- Renders label `Specialist: {specialist_type}` and status mapping.
- Edges use `transition_type="fallback"` connecting the parent step node to the subagent specialist node.
- Detail drawer displays subagent reasoning summaries, findings, and suggestions.
