# Operational Governance Plane & Tenant Policy Controls

Describes system configuration interfaces for admin rules.

## 1. Auditing Modifications
- Every policy setting update is tracked in `GovernancePolicyChange` revision histories.
- Admins can retrieve audit trails to inspect or roll back fields.

## 2. Policy Enforcement
- TenantAgentPolicy: Gated switches enabling subagent availability.
- TenantAlertRule: Mutes specific alert triggers.
- TenantCopilotConfig: Limits voice transcript processing.
