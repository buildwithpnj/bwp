# Collaboration Graph Representation

Renders multi-agent branches in the visual step graph diagram.

## 1. Visual Node properties
- Multi-agent collaboration sessions are projected as subnodes: `node_{workflow_run_id}_collab_{collab_id}`.
- Labels list the participating agents (e.g., `Collaboration: CodeReviewerAgent, DatabaseAuditorAgent`).
- Node status matches the outcome: `"merged"` (success) or `"failed"`.
- Connected to parent step via `transition_type="fallback"` edge.
