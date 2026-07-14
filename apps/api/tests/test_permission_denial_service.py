from app.services.permission_denial_service import PermissionDenialService

def test_handle_denial():
    res = PermissionDenialService.handle_denial("reveal_sensitive_config")
    assert "Status: Blocked" in res
    assert "Action: Reveal Sensitive Config" in res
    assert "This request is blocked by policy." in res
