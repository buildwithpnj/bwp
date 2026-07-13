from typing import List, Dict, Any

class EvidenceGapDetector:
    @classmethod
    def find_gaps(cls, query: str, chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Scans for semantic words from query that are completely absent from document chunks.
        """
        words = query.lower().split()
        absent = []
        all_text = " ".join(c["chunk_text"].lower() for c in chunks)
        
        for w in words:
            if len(w) > 4 and w not in all_text:
                absent.append(w)
        return absent
