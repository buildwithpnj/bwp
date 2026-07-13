from fastapi import APIRouter, HTTPException, Depends, status
from app.deps import CurrentUser, DB
from app.schemas.action_plan import ActionPlan
from app.services.action_planner import ActionPlanner
from app.services.plan_validator import PlanValidator
from app.services.workflow_execution_service import WorkflowExecutionService
from app.services.workflow_state_manager import WorkflowStateManager

router = APIRouter(prefix="/api/workflows", tags=["Agent Workflow Orchestration"])

@router.post("/propose", response_model=ActionPlan, status_code=status.HTTP_200_OK)
async def propose_workflow_plan(
    goal: str,
    current_user: CurrentUser
):
    """
    Translates a human goal query into a structured bounded plan.
    """
    plan = ActionPlanner.propose_plan(goal, current_user.id)
    return plan

@router.post("/execute", status_code=status.HTTP_200_OK)
async def execute_workflow_plan(
    plan: ActionPlan,
    current_user: CurrentUser,
    db: DB
):
    """
    Validates a proposed plan, spawns a WorkflowRun, and triggers execution.
    """
    # 1. Validation
    is_valid, err_msg = PlanValidator.validate_plan(plan, current_user.role)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan validation failed: {err_msg}"
        )
        
    # 2. Convert plan steps to dicts for DB JSON storage
    steps_list = [{"action_name": s.action_name, "payload": s.payload} for s in plan.steps]
    
    # 3. Create run
    wf = await WorkflowExecutionService.create_workflow_run(
        db=db,
        goal=plan.goal,
        reasoning=plan.reasoning_summary,
        steps=steps_list,
        user_role=current_user.role,
        autonomy_tier=1  # Default tier
    )
    
    # 4. Start execution
    res = await WorkflowExecutionService.start_workflow(db, wf.id, current_user.id)
    return res

@router.post("/approve/{wf_id}", status_code=status.HTTP_200_OK)
async def approve_workflow_checkpoint(
    wf_id: str,
    current_user: CurrentUser,
    db: DB
):
    """
    Approves the checkpoint pause on a workflow run and resumes execution.
    """
    res = await WorkflowStateManager.approve_and_resume(db, wf_id, current_user.id)
    if res.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message")
        )
    return res
