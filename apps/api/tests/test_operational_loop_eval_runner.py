import pytest
from app.services.operational_loop_eval_runner import OperationalLoopEvalRunner

@pytest.mark.asyncio
async def test_operational_loop_eval_runner():
    report = await OperationalLoopEvalRunner.run_operational_evals()
    assert report["total_cases"] > 0
    assert report["pass_rate"] >= 0.0
    assert "no_progress" in report["results"]
