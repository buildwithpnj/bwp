class ApprovalGateService:
    _approvals = {}

    @classmethod
    def approve(cls, action_name: str) -> None:
        cls._approvals[action_name] = True

    @classmethod
    def is_approved(cls, action_name: str) -> bool:
        return cls._approvals.get(action_name, False)
