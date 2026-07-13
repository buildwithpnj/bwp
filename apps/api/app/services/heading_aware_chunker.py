import re
from typing import List, Dict

class HeadingAwareChunker:
    @classmethod
    def split_by_headings(cls, text: str) -> List[Dict[str, str]]:
        """
        Splits markdown-first text by structural headers.
        """
        chunks = []
        if not text:
            return chunks
            
        # Matches markdown headers like #, ##, ###
        parts = re.split(r'(^|\n)(?=#+\s)', text)
        current_heading = "root"
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if part.startswith("#"):
                # Extract header title
                header_line = part.split("\n", 1)[0]
                current_heading = header_line.replace("#", "").strip()
                
            chunks.append({
                "heading": current_heading,
                "text": part
            })
        return chunks
