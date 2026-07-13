class UnsupportedClaimBlocker:
    @classmethod
    def block_fabricated_content(cls, raw_answer: str) -> str:
        """
        Replaces fabricated answers with standard abstention statement.
        """
        return "I cannot verify these statements against the retrieved workspace documents. Abstaining from answering."
