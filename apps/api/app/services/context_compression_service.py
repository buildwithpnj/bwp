from typing import List, Dict, Any

class ContextCompressionService:
    @classmethod
    def compress_pack(cls, pack: Dict[str, Any], token_limit: int = 150) -> Dict[str, Any]:
        """
        Compresses evidence chunk text to adhere to token budget limits.
        """
        compressed_blocks = []
        current_tokens = 0
        
        for block in pack.get("evidence_blocks", []):
            words = block["text"].split()
            # truncate words to match token limit parameters
            if current_tokens + len(words) > token_limit:
                remaining = token_limit - current_tokens
                if remaining > 0:
                    truncated_text = " ".join(words[:remaining]) + "..."
                    compressed_blocks.append({
                        "chunk_id": block["chunk_id"],
                        "text": truncated_text,
                        "summary": block["summary"]
                    })
                break
            else:
                compressed_blocks.append(block)
                current_tokens += len(words)
                
        return {
            "query": pack["query"],
            "evidence_blocks": compressed_blocks
        }
