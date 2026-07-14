from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.services.approval_token_service import ApprovalTokenService
from app.services.approval_request_service import ApprovalRequestService

class ApprovalGateService:
    @classmethod
    def validate_approval_token(
        cls, 
        token: str, 
        user_id: str, 
        tenant_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Validates the single-use token against the user/tenant context and returns
        the associated approval_id if successful, burning the token.
        """
        return ApprovalTokenService.validate_and_burn_token(token, user_id, tenant_id)

    @classmethod
    async def is_request_approved(
        cls, 
        db: AsyncSession, 
        approval_id: str
    ) -> bool:
        """
        Checks if the ActionApprovalRequest in the database is in the approved state.
        """
        req = await ApprovalRequestService.get_request(db, approval_id)
        if not req:
            return False
        return req.status == "approved"
