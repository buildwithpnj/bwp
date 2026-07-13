class ActionExecutionStatus:
    SUGGESTED = "suggested"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    QUEUED = "queued"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    PERMANENTLY_FAILED = "permanently_failed"

class ActionRecoveryStatus:
    NONE = "none"
    PENDING_RECOVERY = "pending_recovery"
    RECOVERED = "recovered"
    RECOVERY_FAILED = "recovery_failed"
