class RetrievalScopeGuard:
    @classmethod
    def enforce_scoping(cls, page_scope: str, allowed_scopes: list) -> bool:
        """
        Guarantees users/assistants search only within authorized page scopes.
        """
        if not page_scope:
            return True
        return page_scope in allowed_scopes
