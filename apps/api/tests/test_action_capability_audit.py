import pytest
from app.services.action_capability_audit_service import ActionCapabilityAuditService
from app.services.action_registry_inspector import ActionRegistryInspector

def test_audit_capabilities_report():
    report = ActionCapabilityAuditService.audit_capabilities()
    assert "total_registered" in report
    assert isinstance(report["working_actions"], list)
    assert isinstance(report["blocked_actions"], list)

def test_registry_inspector_validations():
    inspections = ActionRegistryInspector.inspect_registry()
    assert isinstance(inspections, list)
    for item in inspections:
        assert "action_name" in item
        assert "has_schema" in item
        assert "issues" in item
