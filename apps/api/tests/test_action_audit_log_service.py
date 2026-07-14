from app.services.action_audit_log_service import ActionAuditLogService

def test_log_execution():
    action = "update_task"
    payload = {"task_id": "task_123", "status": "completed"}
    tenant = "tenant_xyz"
    
    log_id = ActionAuditLogService.log_execution(action, payload, tenant)
    
    assert log_id in ActionAuditLogService._logs
    entry = ActionAuditLogService._logs[log_id]
    assert entry["action"] == action
    assert entry["payload"] == payload
    assert entry["tenant_id"] == tenant
    assert entry["status"] == "logged"
