class ActionPolicyRegistry:
    _registry = {
        "create_note": "safe_auto",
        "fail_action": "safe_auto",
        "delete_all_files": "confirm_first"
    }

    @classmethod
    def get_policy(cls, action_name: str) -> str:
        return cls._registry.get(action_name, "confirm_first")
