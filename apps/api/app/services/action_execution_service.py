from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from app.models.action_models import ActionLog
from app.models.action_execution_state import ActionExecutionStatus
from app.services.action_registry import ActionRegistry
from app.services.copilot_action_registry import CopilotActionRegistry
from app.services.action_policy_registry import ActionPolicyTier
from app.services.action_approval_service import ActionApprovalService
from app.services.idempotency_guard import IdempotencyGuard, DuplicateRequestException
from app.services.job_enqueuer import JobEnqueuer
from datetime import datetime, timezone


class ActionExecutionService:
    @classmethod
    async def request_execution(
        cls, 
        db: AsyncSession, 
        user_id: str, 
        user_role: str, 
        action_name: str, 
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validates, logs, and queues action executions based on configurations."""
        now = datetime.now(timezone.utc)

        # 1. Enforce preview/private boundary
        if user_role not in ["approved_user", "internal_admin"]:
            return {"status": "failed", "error": "Action execution restricted to approved users."}

        # 2. Check Action Registry Definitions
        action = CopilotActionRegistry.get_action(action_name) or ActionRegistry.get_action(action_name)
        if not action:
            return {"status": "failed", "error": "Action not found."}

        # 3. Validate input schemas parameters
        is_valid = False
        if CopilotActionRegistry.get_action(action_name):
            is_valid = CopilotActionRegistry.validate_inputs(action_name, payload)
        else:
            is_valid = ActionRegistry.validate_inputs(action_name, payload)
            
        if not is_valid:
            return {"status": "failed", "error": "Input payload schema validation failed."}

        # 4. Check role rights gating
        if user_role not in action["allowed_roles"]:
            return {"status": "failed", "error": "Unauthorized role context."}

        # 5. Idempotency guard — block duplicate in-flight or succeeded executions
        from app.llm_settings import llm_settings
        idempotency_key = None
        if llm_settings.idempotency_guard_enabled:
            try:
                idempotency_key, is_new = await IdempotencyGuard.validate_and_gate(
                    db, user_id, action_name, payload
                )
            except DuplicateRequestException as e:
                return {"status": "failed", "error": f"Duplicate request: {str(e)}", "idempotency_blocked": True}
        else:
            import uuid
            idempotency_key = str(uuid.uuid4())

        # 6. Create durable execution audit log with lifecycle timestamps
        log = ActionLog(
            user_id=user_id,
            action_name=action_name,
            input_payload=payload,
            status="pending",
            approval_status="auto_approved",
            idempotency_key=idempotency_key,
            suggested_at=now,
            execution_status=ActionExecutionStatus.SUGGESTED,
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)

        # 7. Check manual approval rules
        if llm_settings.approval_gates_enabled and action["requires_approval"]:
            log.approval_status = "pending"
            log.execution_status = ActionExecutionStatus.PENDING_APPROVAL
            await db.commit()
            approval = await ActionApprovalService.create_approval_request(db, log.id, user_id)
            return {
                "status": "pending_approval",
                "action_log_id": log.id,
                "approval_id": approval.id,
                "message": "Action execution is pending user approval.",
            }

        # 8. Auto-approve: stamp lifecycle timestamps and enqueue
        log.approved_at = now
        log.queued_at = now
        log.execution_status = ActionExecutionStatus.QUEUED
        await db.commit()

        job_id = await JobEnqueuer.enqueue_action(
            action_log_id=log.id,
            action_name=action_name,
            user_id=user_id,
            idempotency_key=idempotency_key,
        )

        return {"status": "queued", "job_id": job_id, "action_log_id": log.id}

    @classmethod
    async def execute_log_action(cls, db: AsyncSession, log: ActionLog) -> Dict[str, Any]:
        from app.services.actions.save_corrected_example import SaveCorrectedExampleAction
        from app.services.actions.create_lesson_note import CreateLessonNoteAction
        from app.services.actions.update_preference import UpdatePreferenceAction
        from app.services.actions.mark_pattern_mastered import MarkPatternMasteredAction
        from app.services.actions.create_followup_practice import CreateFollowupPracticeAction
        from app.services.actions.create_note import CreateNoteAction
        from app.services.actions.update_note import UpdateNoteAction
        from app.services.actions.create_task import CreateTaskAction
        from app.services.actions.update_task import UpdateTaskAction
        from app.services.actions.complete_task import CompleteTaskAction
        from app.services.actions.create_project_item import CreateProjectItemAction
        from app.services.actions.update_project_item import UpdateProjectItemAction
        from app.services.actions.create_calendar_event import CreateCalendarEventAction
        from app.services.actions.create_memory_item import CreateMemoryItemAction
        from app.services.actions.search_knowledge import SearchKnowledgeAction
        from app.services.actions.get_recent_updates import GetRecentUpdatesAction

        # New v0.50 executors
        from app.services.actions.v050_executors import (
            DeleteNoteAction, RestoreNoteAction, SearchNotesAction,
            PrioritizeTaskAction, DeleteTaskAction, RestoreTaskAction,
            CreateProjectAction, UpdateProjectAction, CompleteProjectAction, DeleteProjectAction,
            CreateBookAction, UpdateBookProgressAction, ArchiveBookAction, DeleteBookAction,
            CreateAssetAction, UpdateAssetAction, DeleteAssetAction,
            UploadMediaMetadataAction, UpdateMediaMetadataAction, DeleteMediaMetadataAction,
            GetStorageStatusAction, CleanupStorageAction,
            UpdateCalendarEventAction, CancelCalendarEventAction,
            CreateHabitAction, LogHabitCheckinAction, DeleteHabitAction,
            CreateAddictionTrackerAction, LogAddictionRelapseAction, GetSobrietyStatsAction,
            UpdateMemoryItemAction, DeleteMemoryItemAction,
            CreateKnowledgeItemAction, DeleteKnowledgeItemAction,
            GetTelemetryStatusAction, TriggerSystemSyncAction,
            UpdateReminderPreferencesAction,
            ListTrashItemsAction, RestoreTrashItemAction, PermanentPurgeItemAction
        )

        executors: Dict[str, Any] = {
            "save_corrected_example": SaveCorrectedExampleAction,
            "create_lesson_note": CreateLessonNoteAction,
            "update_preference": UpdatePreferenceAction,
            "mark_pattern_mastered": MarkPatternMasteredAction,
            "create_followup_practice": CreateFollowupPracticeAction,
            "create_note": CreateNoteAction,
            "update_note": UpdateNoteAction,
            "create_task": CreateTaskAction,
            "update_task": UpdateTaskAction,
            "complete_task": CompleteTaskAction,
            "create_project_item": CreateProjectItemAction,
            "update_project_item": UpdateProjectItemAction,
            "create_calendar_event": CreateCalendarEventAction,
            "create_memory_item": CreateMemoryItemAction,
            "search_knowledge": SearchKnowledgeAction,
            "get_recent_updates": GetRecentUpdatesAction,

            # New v0.50 executors registration
            "delete_note": DeleteNoteAction,
            "restore_note": RestoreNoteAction,
            "search_notes": SearchNotesAction,
            "prioritize_task": PrioritizeTaskAction,
            "delete_task": DeleteTaskAction,
            "restore_task": RestoreTaskAction,
            "create_project": CreateProjectAction,
            "update_project": UpdateProjectAction,
            "complete_project": CompleteProjectAction,
            "delete_project": DeleteProjectAction,
            "create_book": CreateBookAction,
            "update_book_progress": UpdateBookProgressAction,
            "archive_book": ArchiveBookAction,
            "delete_book": DeleteBookAction,
            "create_asset": CreateAssetAction,
            "update_asset": UpdateAssetAction,
            "delete_asset": DeleteAssetAction,
            "upload_media_metadata": UploadMediaMetadataAction,
            "update_media_metadata": UpdateMediaMetadataAction,
            "delete_media_metadata": DeleteMediaMetadataAction,
            "get_storage_status": GetStorageStatusAction,
            "cleanup_storage": CleanupStorageAction,
            "update_calendar_event": UpdateCalendarEventAction,
            "cancel_calendar_event": CancelCalendarEventAction,
            "create_habit": CreateHabitAction,
            "log_habit_checkin": LogHabitCheckinAction,
            "delete_habit": DeleteHabitAction,
            "create_addiction_tracker": CreateAddictionTrackerAction,
            "log_addiction_relapse": LogAddictionRelapseAction,
            "get_sobriety_stats": GetSobrietyStatsAction,
            "update_memory_item": UpdateMemoryItemAction,
            "delete_memory_item": DeleteMemoryItemAction,
            "create_knowledge_item": CreateKnowledgeItemAction,
            "delete_knowledge_item": DeleteKnowledgeItemAction,
            "get_telemetry_status": GetTelemetryStatusAction,
            "trigger_system_sync": TriggerSystemSyncAction,
            "update_reminder_preferences": UpdateReminderPreferencesAction,
            "list_trash_items": ListTrashItemsAction,
            "restore_trash_item": RestoreTrashItemAction,
            "permanent_purge_item": PermanentPurgeItemAction
        }

        executor = executors.get(log.action_name)
        if not executor:
            log.status = "failed"
            log.error_message = "Executor mapping not found."
            await db.commit()
            return {"status": "failed", "error": log.error_message}

        try:
            res = await executor.execute(db, log.user_id, log.input_payload)
            log.status = "success"
            log.result_payload = res
            log.completed_at = datetime.now(timezone.utc)
            await db.commit()
            return res
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            log.completed_at = datetime.now(timezone.utc)
            await db.commit()
            return {"status": "failed", "error": log.error_message}

    @classmethod
    def execute_action(cls, action_name: str, payload: Dict[str, Any], tenant_id: str) -> Dict[str, Any]:
        """
        Executes writes with policy classifications and rollback safeguards.
        """
        from app.services.action_policy_registry import ActionPolicyRegistry
        from app.services.approval_gate_service import ApprovalGateService
        from app.services.action_audit_log_service import ActionAuditLogService
        from app.services.rollback_service import RollbackService

        policy = ActionPolicyRegistry.get_policy(action_name)
        from app.llm_settings import llm_settings
        if policy == "confirm_first" and llm_settings.approval_gates_enabled:
            if not ApprovalGateService.is_approved(action_name):
                return {"status": "pending_approval", "action": action_name}
                
        # Record audit log
        log_id = ActionAuditLogService.log_execution(action_name, payload, tenant_id)
        
        try:
            # Simulate successful write execution
            if action_name == "fail_action":
                raise RuntimeError("Simulated action writing failure.")
            return {"status": "success", "log_id": log_id}
        except Exception as e:
            # Perform automatic compensation rollback
            RollbackService.trigger_rollback(action_name, payload, tenant_id)
            return {"status": "rolled_back", "error": str(e)}
