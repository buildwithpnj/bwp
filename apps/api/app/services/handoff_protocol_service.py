import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from app.models.collaboration_handoff import CollaborationHandoff
from app.services.collaboration_contract_validator import CollaborationContractValidator

logger = logging.getLogger("handoff_protocol_service")

class HandoffProtocolService:
    # Allowed handoff pathways to prevent arbitrary loops
    _allowed_paths = {
        ("CodeReviewerAgent", "DatabaseAuditorAgent"),
        ("DatabaseAuditorAgent", "WorkflowDiagnosticianAgent"),
        ("WorkflowDiagnosticianAgent", "SafetyPolicyCheckerAgent")
    }

    @classmethod
    async def process_handoff(
        cls,
        db: AsyncSession,
        collaboration_run_id: str,
        sender: str,
        receiver: str,
        payload: Dict[str, Any]
    ) -> bool:
        """
        Validates sender/receiver pairs, verifies payload contracts, and logs a CollaborationHandoff.
        """
        # 1. Path check
        if (sender, receiver) not in cls._allowed_paths:
            logger.warning(f"Handoff Blocked: Pathway '{sender} -> {receiver}' not authorized.")
            return False
            
        # 2. Contract check
        valid = CollaborationContractValidator.validate_payload(sender, receiver, payload)
        status = "accepted" if valid else "rejected"
        
        # 3. Log Handoff
        handoff = CollaborationHandoff(
            collaboration_run_id=collaboration_run_id,
            sender_agent=sender,
            receiver_agent=receiver,
            payload_contract=payload,
            handoff_status=status
        )
        db.add(handoff)
        await db.commit()
        
        logger.info(f"Handoff processed: {sender} -> {receiver} status={status}")
        return valid
