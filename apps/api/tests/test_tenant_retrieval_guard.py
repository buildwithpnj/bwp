import pytest
from app.services.tenant_retrieval_guard import TenantRetrievalGuard

def test_tenant_retrieval_guard():
    TenantRetrievalGuard.validate_tenant("tenant_123")
    
    with pytest.raises(PermissionError):
        TenantRetrievalGuard.validate_tenant("")
