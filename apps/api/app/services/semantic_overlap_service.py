class SemanticOverlapService:
    @classmethod
    def attach_context_buffer(cls, chunks: list, overlap_count: int = 1) -> list:
        """
        Injects leading context text from previous chunk indices.
        """
        buffered = []
        for i, chunk in enumerate(chunks):
            prefix = ""
            if i > 0 and overlap_count > 0:
                prev_text = chunks[i - 1]["text"]
                # Append last 100 characters of previous chunk
                prefix = prev_text[-100:] + " [...] "
            buffered.append({
                "heading": chunk["heading"],
                "text": prefix + chunk["text"]
            })
        return buffered
