import pytest
from unittest.mock import AsyncMock
from app.services.plan_simulation_service import PlanSimulationService
from app.schemas.simulation_request import SimulationRequest

@pytest.mark.asyncio
async def test_plan_evaluation_in_sandbox():
    db = AsyncMock()
    
    # Preflight candidate steps
    steps = [
        {"action_name": "create_lesson_note", "payload": {"content": ""}}, # Fails content check
        {"action_name": "build_practice_plan", "payload": {"focus_area": "algebra"}}
    ]
    
    req = SimulationRequest(workflow_run_id="wf_sim_1", plan_steps=steps)
    res = await PlanSimulationService.simulate_plan(db, req)
    
    # 1 check should fail
    assert len(res.likely_failures) == 1
    assert "content" in res.likely_failures[0]
    
    # Success rate should be penalised
    assert res.predicted_success_score == 0.7
    assert res.risk_score == 0.4
