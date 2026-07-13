from app.schemas.delegation_response_schema import DelegationResponse

class DelegationResultValidator:
    @classmethod
    def validate(cls, resp: DelegationResponse) -> bool:
        """
        Validates the specialist response against systemic schemas constraint bounds.
        """
        if not resp.delegation_id:
            return False
        if resp.confidence_score < 0.0 or resp.confidence_score > 1.0:
            return False
        if not resp.specialist_type:
            return False
        return True
