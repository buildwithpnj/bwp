import re

class LogSignalExtractor:
    @classmethod
    def extract_error_code(cls, log_text: str) -> str:
        """
        Regex parses log strings to identify errors.
        """
        match = re.search(r"error_code=(\w+)", log_text)
        if match:
            return match.group(1)
        return "unknown"
