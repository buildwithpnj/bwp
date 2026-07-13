from app.services.grounding_eval_runner import GroundingEvalRunner

def test_grounding_eval_runner():
    res = GroundingEvalRunner.execute_grounding_eval("nonexistent_dataset.json")
    assert res["status"] == "skipped"
