from typing import Dict, Any

class MetadataFilterBuilder:
    @classmethod
    def build_tenant_filters(cls, tenant_id: str, scope: str = None) -> Dict[str, Any]:
        """
        Builds and validates tenant-isolated filter expressions.
        """
        if not tenant_id:
            raise ValueError("Tenant scope ID cannot be null or empty.")
            
        filters = {"tenant_id": tenant_id}
        if scope:
            if scope not in ["internal", "external", "public"]:
                raise ValueError("Invalid visibility scope parameter value.")
            filters["visibility_scope"] = scope
        return filters
