import logging
from typing import Dict, Optional
from app.schemas.subagent_capability_schema import SubAgentCapability

logger = logging.getLogger("subagent_registry")

class SubAgentRegistry:
    # Specialist Registry mapping to capability definitions
    _specialists: Dict[str, SubAgentCapability] = {
        "CodeReviewerAgent": SubAgentCapability(
            specialist_type="CodeReviewerAgent",
            purpose="Audits Python models and services for security or compilation errors.",
            allowed_input_domains=["code", "schemas", "models"],
            max_delegation_steps=3,
            allowed_tools=["grep_search", "view_file"],
            risk_level="low",
            token_budget_cap=5.0,
            timeout_ms=5000
        ),
        "DatabaseAuditorAgent": SubAgentCapability(
            specialist_type="DatabaseAuditorAgent",
            purpose="Inspects transaction scopes, indices, and schema migrations.",
            allowed_input_domains=["database", "migrations", "locks"],
            max_delegation_steps=3,
            allowed_tools=["db_query_dry_run"],
            risk_level="medium",
            token_budget_cap=3.0,
            timeout_ms=4000
        ),
        "WorkflowDiagnosticianAgent": SubAgentCapability(
            specialist_type="WorkflowDiagnosticianAgent",
            purpose="Analyzes repeating retry failures, stalled approvals, and recovery paths.",
            allowed_input_domains=["workflow_history", "failure_patterns"],
            max_delegation_steps=5,
            allowed_tools=["get_workflow_trace_log"],
            risk_level="low",
            token_budget_cap=4.0,
            timeout_ms=6000
        ),
        "SafetyPolicyCheckerAgent": SubAgentCapability(
            specialist_type="SafetyPolicyCheckerAgent",
            purpose="Verifies validation policies, role gates, and tenant access isolation.",
            allowed_input_domains=["auth_roles", "policies", "tenant_isolation"],
            max_delegation_steps=2,
            allowed_tools=["check_gating_rules"],
            risk_level="high",
            token_budget_cap=2.0,
            timeout_ms=3000
        )
    }

    @classmethod
    def get_specialist(cls, name: str) -> Optional[SubAgentCapability]:
        return cls._specialists.get(name)

    @classmethod
    def list_specialists(cls) -> Dict[str, SubAgentCapability]:
        return cls._specialists
