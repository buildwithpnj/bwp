class ToolPolicyGuard:
    @classmethod
    def is_tool_allowed(cls, tool_name: str, requested_mode: str) -> bool:
        """
        Assures read-only restriction guards are respected.
        """
        if requested_mode == "write" and tool_name not in ["create_note", "create_task", "tag_document"]:
            return False
        return True
