import re
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("structured_output_repair")

class StructuredOutputRepairService:
    @classmethod
    def clean_and_repair_json(cls, raw_text: str) -> str:
        """
        Sanitizes and repairs common malformed JSON strings emitted by local inference models.
        """
        cleaned = raw_text.strip()
        
        # 1. Strip markdown code fences if present (e.g. ```json ... ```)
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        # 2. Fix trailing commas inside dictionaries and lists
        # match comma followed by whitespace and closing brace/bracket
        cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

        # 3. Handle simple string truncation: append missing closing brackets/braces
        if cleaned.startswith("{") and not cleaned.endswith("}"):
            # check if open braces count > closed
            open_count = cleaned.count("{")
            close_count = cleaned.count("}")
            if open_count > close_count:
                cleaned += "}" * (open_count - close_count)
        elif cleaned.startswith("[") and not cleaned.endswith("]"):
            open_count = cleaned.count("[")
            close_count = cleaned.count("]")
            if open_count > close_count:
                cleaned += "]" * (open_count - close_count)
                
        return cleaned

    @classmethod
    def parse_repaired_json(cls, raw_text: str) -> Optional[Any]:
        """
        Attempts to parse JSON, applying repair heuristics on failure.
        """
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            repaired = cls.clean_and_repair_json(raw_text)
            try:
                parsed = json.loads(repaired)
                logger.info("Successfully repaired and parsed local model JSON output.")
                return parsed
            except json.JSONDecodeError as e:
                logger.error(f"Structured JSON repair failed. Repaired string: '{repaired}'. Error: {e}")
                return None
