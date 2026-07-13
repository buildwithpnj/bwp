from typing import List, Dict, Any

class CitationAlignmentService:
    @classmethod
    def align_citations(cls, answer: str, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculates search match indices inside the generated answer text.
        """
        aligned = []
        for cit in citations:
            text = cit.get("citation_text") or ""
            start = answer.lower().find(text.lower())
            if start != -1:
                aligned.append({
                    "document_id": cit["document_id"],
                    "chunk_id": cit["chunk_id"],
                    "citation_text": text,
                    "span_start": start,
                    "span_end": start + len(text)
                })
            else:
                aligned.append({
                    "document_id": cit["document_id"],
                    "chunk_id": cit["chunk_id"],
                    "citation_text": text,
                    "span_start": 0,
                    "span_end": 0
                })
        return aligned
