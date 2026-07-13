import re

class DocumentCleaningService:
    @classmethod
    def clean_text(cls, text: str) -> str:
        """
        Cleans and normalizes document text content by removing extra spaces.
        """
        if not text:
            return ""
        # Remove repeated whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', text)
        return cleaned.strip()
