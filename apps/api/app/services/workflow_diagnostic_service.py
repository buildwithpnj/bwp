import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.workflow_run import WorkflowRun
from app.models.action_models import ActionLog
from app.models.workflow_diagnostic_report import WorkflowDiagnosticReport
from app.services.failure_pattern_service import FailurePatternService
from app.services.context_aware_diagnostic_builder import ContextAwareDiagnosticBuilder
from app.services.recovery_suggestion_service import RecoverySuggestionService

logger = logging.getLogger("workflow_diagnostic_service")

class WorkflowDiagnosticService:
    @classmethod
    async def generate_report(
        cls,
        db: AsyncSession,
        workflow_run_id: str,
        action_log_id: Optional[str] = None
    ) -> Optional[WorkflowDiagnosticReport]:
        """
        Gathers logs, runs diagnostics checks, generates ranked recovery options,
        and saves a new WorkflowDiagnosticReport record to the database.
        """
        # 1. Fetch Workflow
        wf_stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        wf_res = await db.execute(wf_stmt)
        wf = wf_res.scalar_one_or_none()
        
        if not wf:
            logger.error(f"Cannot diagnose: Workflow run {workflow_run_id} not found.")
            return None
            
        # 2. Find failed action log
        target_log_id = action_log_id
        if not target_log_id:
            # Find the latest failed log for this user/workflow run
            log_stmt = select(ActionLog).where(
                ActionLog.user_id == wf.steps[0]["payload"].get("user_id", "system") if wf.steps else "system",
                ActionLog.status == "failed"
            ).order_by(ActionLog.created_at.desc()).limit(1)
            log_res = await db.execute(log_stmt)
            latest_failed_log = log_res.scalar_one_or_none()
            if latest_failed_log:
                target_log_id = latest_failed_log.id
                
        # 3. Load target log
        log = None
        if target_log_id:
            log_stmt = select(ActionLog).where(ActionLog.id == target_log_id)
            log_res = await db.execute(log_stmt)
            log = log_res.scalar_one_or_none()
            
        if not log:
            # Create a mock/generic log if none exists to avoid crashes
            log = ActionLog(
                id="log_fallback",
                user_id="user_123",
                action_name=wf.steps[wf.current_step_index]["action_name"] if wf.steps else "unknown",
                error_message="Workflow execution halted during processing.",
                retry_count=0
            )

        # 4. Analyze patterns and compile diagnostics
        patterns = FailurePatternService.analyze_patterns(log)
        diag_details = ContextAwareDiagnosticBuilder.compile_diagnostics(log, patterns)
        
        # 5. Generate and rank recovery suggestions
        recovery_options = await RecoverySuggestionService.generate_and_rank_suggestions(
            db, wf, log, patterns
        )
        
        # 6. Save report
        report = WorkflowDiagnosticReport(
            workflow_run_id=workflow_run_id,
            action_log_id=log.id,
            diagnostic_type="repeated_retry_pattern" if "repeated_retry_pattern" in patterns else "execution_failure",
            severity=diag_details["severity"],
            likely_causes=diag_details["likely_causes"],
            evidence_points=diag_details["evidence_points"],
            suggested_recovery_options=[opt.model_dump() for opt in recovery_options],
            confidence_score=0.9 if "repeated_retry_pattern" in patterns else 0.7,
            requires_human_review=True
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        
        logger.info(f"Diagnostic report generated: ID={report.id} type={report.diagnostic_type}")
        return report
