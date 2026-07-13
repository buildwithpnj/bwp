from typing import List, Dict, Any

class EvidencePackBuilder:
    @classmethod
    def assemble_pack(cls, query: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assembles sorted evidence blocks.
        """
        return {
            "query": query,
            "evidence_blocks": [
                {
                    "chunk_id": c["chunk_id"],
                    "text": c["chunk_text"],
                    "summary": c["chunk_summary"]
                }
                for c in chunks
            ]
        }
