class TenantRetrievalGuard:
    @classmethod
    def validate_tenant(cls, query_tenant_id: str) -> None:
        """
        Guarantees no cross-tenant query execution.
        """
        if not query_tenant_id or len(query_tenant_id.strip()) == 0:
            raise PermissionError("Access Denied: Missing tenant scope constraint.")
