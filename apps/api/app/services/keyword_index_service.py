import re
from typing import Set

class KeywordIndexService:
    @classmethod
    def extract_keywords(cls, text: str) -> Set[str]:
        """
        Tokenizes text parameters and extracts lexical search keys.
        """
        if not text:
            return set()
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return set(words)
