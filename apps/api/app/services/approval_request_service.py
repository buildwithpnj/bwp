from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
import uuid
import json

from app.models.action_approval_models import ActionApprovalRequest
from app.services.action_risk_classifier import ActionRiskClassifier
from app.services.action_policy_registry import ActionPolicyTier
from app.services.copilot_action_registry import CopilotActionRegistry

class ApprovalRequestService:
    @classmethod
    async def create_request(
        cls, 
        db: AsyncSession, 
        user_id: str, 
        action_name: str, 
        payload: Dict[str, Any], 
        tenant_id: Optional[str] = None,
        session_id: Optional[str] = None,
        action_log_id: Optional[str] = None,
        expiry_minutes: int = 10
    ) -> ActionApprovalRequest:
        """
        Creates a new ActionApprovalRequest based on action name, payload, and risk classification.
        """
        # Classify policy and risk level
        policy_tier = ActionRiskClassifier.classify_action(action_name, payload)
        
        # Risk level determination based on policy tier
        if policy_tier == ActionPolicyTier.SAFE_AUTO:
            risk_level = "safe"
        elif policy_tier == ActionPolicyTier.CONFIRM_FIRST:
            risk_level = "medium"
        elif policy_tier == ActionPolicyTier.DESTRUCTIVE_CONFIRMED:
            risk_level = "high"
        else:
            risk_level = "critical"

        # Resolve module name from registry
        action_meta = CopilotActionRegistry.get_action(action_name) or {}
        module_name = action_meta.get("module", "general")

        # Dynamically extract target type and target ID from payload keys
        target_type = None
        target_id = None
        
        for key in ["note_id", "task_id", "project_id", "book_id", "asset_id", "event_id", "habit_id", "tracker_id", "memory_id", "resource_id", "credential_id"]:
            if key in payload:
                target_type = key.replace("_id", "")
                target_id = str(payload[key])
                break
        
        if not target_type and "item_id" in payload:
            target_type = payload.get("item_type", "item")
            target_id = str(payload["item_id"])

        # Construct human readable summary and execution preview
        human_summary = f"Request to execute action '{action_name}' on {target_type or 'general'} target."
        if action_name == "delete_note":
            human_summary = f"Permanently delete note card: '{payload.get('note_id', '')}'."
        elif action_name == "update_task":
            human_summary = f"Update status of task '{payload.get('task_id', '')}' to '{payload.get('status', '')}'."
            
        execution_preview = f"Action: {action_name}\nPayload: {json.dumps(payload, indent=2)}"

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

        req = ActionApprovalRequest(
            id=f"apr_{uuid.uuid4().hex[:8]}",
            action_log_id=action_log_id,
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            action_name=action_name,
            module_name=module_name,
            policy_tier=policy_tier.value,
            risk_level=risk_level,
            target_type=target_type,
            target_id=target_id,
            action_payload=payload,
            human_summary=human_summary,
            execution_preview=execution_preview,
            expires_at=expires_at,
            status="pending"
        )
        
        db.add(req)
        await db.commit()
        await db.refresh(req)
        return req

    @classmethod
    async def get_request(cls, db: AsyncSession, approval_id: str) -> Optional[ActionApprovalRequest]:
        result = await db.execute(select(ActionApprovalRequest).where(ActionApprovalRequest.id == approval_id))
        return result.scalar_one_or_none()

    @classmethod
    async def update_status(
        cls, 
        db: AsyncSession, 
        approval_id: str, 
        status: str,
        actor_id: Optional[str] = None,
        audit_id: Optional[str] = None
    ) -> bool:
        """
        Safely transition approval request status.
        """
        req = await cls.get_request(db, approval_id)
        if not req:
            return False

        # Expiry check
        if req.status == "pending" and datetime.now(timezone.utc) > req.expires_at:
            req.status = "expired"
            await db.commit()
            
        if req.status != "pending" and status != "expired":
            return False  # Already decided or transitioned

        req.status = status
        if status == "approved":
            req.approved_by = actor_id
        elif status == "denied":
            req.denied_by = actor_id
            
        if audit_id:
            req.audit_id = audit_id
            
        await db.commit()
        return True
