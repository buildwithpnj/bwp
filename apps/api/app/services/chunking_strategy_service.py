from typing import List, Dict
from app.services.heading_aware_chunker import HeadingAwareChunker
from app.services.chunk_quality_service import ChunkQualityService

class ChunkingStrategyService:
    @classmethod
    def segment_document(cls, text: str) -> List[Dict[str, str]]:
        """
        Segments raw canonical document body into high-quality heading-aware chunks.
        """
        raw_chunks = HeadingAwareChunker.split_by_headings(text)
        valid_chunks = []
        
        for item in raw_chunks:
            # Check Quality constraints
            if ChunkQualityService.validate_chunk(item["text"]):
                valid_chunks.append(item)
                
        return valid_chunks
