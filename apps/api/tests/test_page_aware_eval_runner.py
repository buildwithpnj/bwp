from app.services.page_aware_eval_runner import PageAwareEvalRunner

def test_page_aware_eval_runner():
    res = PageAwareEvalRunner.execute_page_aware_eval("nonexistent_dataset.json")
    assert res["status"] == "skipped"
