from app.services.grounding_integrity_checker import GroundingIntegrityChecker

def test_check_hallucination():
    citations = [{"citation_text": "system configuration values"}]
    res = GroundingIntegrityChecker.check_hallucination("we set configuration details", citations)
    assert res is False
