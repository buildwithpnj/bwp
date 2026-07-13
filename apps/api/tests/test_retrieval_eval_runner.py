from app.services.retrieval_eval_runner import RetrievalEvalRunner

def test_retrieval_eval_runner():
    res = RetrievalEvalRunner.execute_eval("nonexistent_dataset.json")
    assert res["status"] == "skipped"
