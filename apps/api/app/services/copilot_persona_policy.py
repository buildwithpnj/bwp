import re

class CopilotPersonaPolicy:
    BANNED_PHRASES = [
        r"how can i assist you today\??",
        r"would you like to proceed\??",
        r"sure!",
        r"great!",
        r"awesome!",
        r"anything else\??"
    ]

    @classmethod
    def sanitize_reply(cls, reply: str) -> str:
        """
        Removes banned chatbot filler phrases and ensures professional tone.
        """
        sanitized = reply
        for pattern in cls.BANNED_PHRASES:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        
        # Clean up double spaces or trailing punctuation
        sanitized = re.sub(r"\s+", " ", sanitized).strip()
        
        if not sanitized:
            return "Review the requested change below."
        return sanitized

    @classmethod
    def scrub_planning_artifacts(cls, text: str) -> str:
        """
        Removes raw action planning text, XML tags, or raw JSON block leaks.
        """
        # Remove XML tags and everything inside them
        text = re.sub(r"<action>.*?</action>", "", text, flags=re.DOTALL)
        text = re.sub(r"<.*?>.*?</.*?>", "", text, flags=re.DOTALL)
        text = re.sub(r"<.*?>", "", text)
        
        # Remove JSON-like blocks
        text = re.sub(r"\{.*?\}", "", text, flags=re.DOTALL)
        
        # Remove raw action blocks like [action: ...]
        text = re.sub(r"\[action.*?\]", "", text, flags=re.IGNORECASE | re.DOTALL)
        
        # Normalize multiple spaces into single space
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()
