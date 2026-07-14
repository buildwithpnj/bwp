import pytest
import time
from app.services.approval_token_service import ApprovalTokenService

def test_token_lifecycle():
    user_id = "user_abc"
    tenant_id = "tenant_xyz"
    approval_id = "apr_123"

    # Generate token
    token = ApprovalTokenService.generate_token(
        approval_id=approval_id,
        user_id=user_id,
        tenant_id=tenant_id,
        expiry_seconds=3
    )
    assert token.startswith("tok_")

    # Validate and burn
    validated_id = ApprovalTokenService.validate_and_burn_token(token, user_id, tenant_id)
    assert validated_id == approval_id

    # Try to reuse (replay attack prevention)
    validated_again = ApprovalTokenService.validate_and_burn_token(token, user_id, tenant_id)
    assert validated_again is None

def test_token_mismatches():
    user_id = "user_abc"
    tenant_id = "tenant_xyz"
    approval_id = "apr_123"

    token = ApprovalTokenService.generate_token(
        approval_id=approval_id,
        user_id=user_id,
        tenant_id=tenant_id
    )

    # Mismatched user
    assert ApprovalTokenService.validate_and_burn_token(token, "other_user", tenant_id) is None

    # Mismatched tenant
    assert ApprovalTokenService.validate_and_burn_token(token, user_id, "other_tenant") is None

def test_token_expiration():
    user_id = "user_abc"
    tenant_id = "tenant_xyz"
    approval_id = "apr_123"

    # Generate short token (expired instantly for test)
    token = ApprovalTokenService.generate_token(
        approval_id=approval_id,
        user_id=user_id,
        tenant_id=tenant_id,
        expiry_seconds=-10
    )
    
    # Try validating expired
    assert ApprovalTokenService.validate_and_burn_token(token, user_id, tenant_id) is None
