import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.simulation_run import SimulationRun
from app.schemas.simulation_request import SimulationRequest
from app.schemas.simulation_result import SimulationResult
from app.services.sandbox_evaluator import SandboxEvaluator
from app.services.plan_risk_scorer import PlanRiskScorer

class PlanSimulationService:
    @classmethod
    async def simulate_plan(
        cls,
        db: AsyncSession,
        req: SimulationRequest
    ) -> SimulationResult:
        """
        Runs plans against virtual read-only sandbox structures, returning simulation metrics.
        """
        likely_failures = SandboxEvaluator.evaluate_plan_failures(req.plan_steps)
        risk = PlanRiskScorer.calculate_plan_risk(req.plan_steps)
        success = 1.0 - (len(likely_failures) * 0.3)
        if success < 0.0:
            success = 0.0
            
        # Log run
        run = SimulationRun(
            id=str(uuid.uuid4()),
            workflow_run_id=req.workflow_run_id,
            plan_steps=req.plan_steps,
            predicted_success_score=success,
            likely_failures=likely_failures,
            risk_score=risk
        )
        db.add(run)
        await db.commit()
        
        return SimulationResult(
            predicted_success_score=success,
            likely_failures=likely_failures,
            risk_score=risk,
            simulated_outcome_summary=f"Simulated execution completed. Success rate={success:.2f} Risk={risk:.2f}."
        )
