import re

class CopilotResponseStyleService:
    # Compile pattern for casual phrases we must purge
    CASUAL_PATTERNS = [
        re.compile(r"\bdone\s*:\)", re.IGNORECASE),
        re.compile(r"\bsure\s+thing\b", re.IGNORECASE),
        re.compile(r"\banything\s+else\??", re.IGNORECASE),
        re.compile(r"\bno\s+problem\b", re.IGNORECASE),
        re.compile(r"\bgot\s+it\b", re.IGNORECASE),
        re.compile(r"\bhere\s+you\s+go\b", re.IGNORECASE)
    ]

    @classmethod
    def sanitize_response(cls, text: str) -> str:
        """
        Strips casual expressions, smiles, and conversational filler,
        returning clean, operational, mature language.
        """
        cleaned = text
        for pattern in cls.CASUAL_PATTERNS:
            cleaned = pattern.sub("", cleaned)
            
        # Clean double spaces or trailing punctuation
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        
        # Ensure it has a professional ending or structure if empty
        if not cleaned:
            cleaned = "Action execution completed."
            
        return cleaned
