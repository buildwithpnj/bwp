import pytest
from app.services.metadata_filter_builder import MetadataFilterBuilder

def test_build_tenant_filters():
    res = MetadataFilterBuilder.build_tenant_filters("tenant_123", "internal")
    assert res["tenant_id"] == "tenant_123"
    assert res["visibility_scope"] == "internal"
    
    with pytest.raises(ValueError):
        MetadataFilterBuilder.build_tenant_filters("", "internal")
