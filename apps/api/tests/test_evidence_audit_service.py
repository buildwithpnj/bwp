from app.services.evidence_audit_service import EvidenceAuditService

def test_audit_evidence():
    chunks = [{"score": 0.85}, {"score": 0.90}]
    res = EvidenceAuditService.audit_evidence(chunks)
    assert res == "strong"
