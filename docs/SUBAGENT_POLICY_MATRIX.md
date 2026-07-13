# Subagent Specialist Policy Matrix

Specialist capabilities, allowed domains, tools, and risk boundaries.

| Specialist Name | Purpose | Allowed Domains | Allowed Tools | Risk Level |
|---|---|---|---|---|
| `CodeReviewerAgent` | Audits code bugs | code, schemas, models | grep_search, view_file | Low |
| `DatabaseAuditorAgent` | Inspects schema locks | database, migrations, locks | db_query_dry_run | Medium |
| `WorkflowDiagnosticianAgent` | Failure pattern audits | workflow_history, failure_patterns | get_workflow_trace_log | Low |
| `SafetyPolicyCheckerAgent` | Verifies gating rules | auth_roles, policies | check_gating_rules | High |
