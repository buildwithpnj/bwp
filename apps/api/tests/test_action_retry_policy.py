from app.services.action_retry_policy import ActionRetryPolicy

def test_retry_policy_repeatable():
    # create_followup_practice allows up to 3 retries
    assert ActionRetryPolicy.should_retry("create_followup_practice", 0) is True
    assert ActionRetryPolicy.should_retry("create_followup_practice", 2) is True
    assert ActionRetryPolicy.should_retry("create_followup_practice", 3) is False

    # create_lesson_note allows up to 2 retries
    assert ActionRetryPolicy.should_retry("create_lesson_note", 0) is True
    assert ActionRetryPolicy.should_retry("create_lesson_note", 1) is True
    assert ActionRetryPolicy.should_retry("create_lesson_note", 2) is False

def test_retry_policy_non_repeatable():
    # update_preference allows 0 retries
    assert ActionRetryPolicy.should_retry("update_preference", 0) is False
    # save_corrected_example allows 0 retries
    assert ActionRetryPolicy.should_retry("save_corrected_example", 0) is False
