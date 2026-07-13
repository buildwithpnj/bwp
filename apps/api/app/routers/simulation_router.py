from fastapi import APIRouter, status
from app.deps import CurrentUser, DB
from app.schemas.simulation_request import SimulationRequest
from app.services.plan_simulation_service import PlanSimulationService

router = APIRouter(prefix="/api/simulation", tags=["Sandboxed Plan Simulation"])

@router.post("/evaluate", status_code=status.HTTP_200_OK)
async def evaluate_candidate_plan(
    req: SimulationRequest,
    current_user: CurrentUser,
    db: DB
):
    """
    Simulates proposed plans in a read-only virtual sandbox to verify dependencies and risk index ratings.
    """
    res = await PlanSimulationService.simulate_plan(db, req)
    return {
        "predicted_success_score": res.predicted_success_score,
        "likely_failures": res.likely_failures,
        "risk_score": res.risk_score,
        "outcome_summary": res.simulated_outcome_summary
    }
