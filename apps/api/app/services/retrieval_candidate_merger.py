from typing import List, Dict, Any

class RetrievalCandidateMerger:
    @classmethod
    def merge_candidates(
        cls,
        lexical_candidates: List[Dict[str, Any]],
        vector_candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merges lexical candidates and vector candidates deterministically.
        Deduplicates matches and constructs a consolidated listing.
        """
        combined = {}
        # Incorporate lexical hits
        for lc in lexical_candidates:
            combined[lc["chunk_id"]] = {
                "chunk_id": lc["chunk_id"],
                "document_id": lc["document_id"],
                "chunk_text": lc["chunk_text"],
                "chunk_summary": lc["chunk_summary"],
                "score": lc.get("score") or 0.6
            }
            
        # Incorporate vector hits (taking maximum score if duplicate exists)
        for vc in vector_candidates:
            cid = vc["chunk_id"]
            score = vc.get("score") or 0.5
            if cid in combined:
                combined[cid]["score"] = max(combined[cid]["score"], score)
            else:
                combined[cid] = {
                    "chunk_id": cid,
                    "document_id": vc["document_id"],
                    "chunk_text": vc["chunk_text"],
                    "chunk_summary": vc["chunk_summary"],
                    "score": score
                }
                
        merged = list(combined.values())
        merged.sort(key=lambda x: x["score"], reverse=True)
        return merged
