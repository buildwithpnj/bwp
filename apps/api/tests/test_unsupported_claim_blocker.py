import pytest
from app.services.unsupported_claim_blocker import UnsupportedClaimBlocker

def test_unsupported_claim_blocker():
    ans = "We deployed V45 loop on AWS today."
    blocked = UnsupportedClaimBlocker.block_fabricated_content(ans)
    assert "Abstaining from answering" in blocked
