class GraphPathExplainer:
    @classmethod
    def get_explanation(cls, source_id: str, target_id: str, relationship: str) -> str:
        """
        Formulates a human-readable tracing explanation for edge traversals.
        """
        return f"Linked from document '{source_id}' to target '{target_id}' via relationship link '{relationship}'."
