import yaml
from typing import Tuple, Dict, Any

class FrontmatterParser:
    @classmethod
    def parse_content(cls, content: str) -> Tuple[Dict[str, Any], str]:
        """
        Parses YAML frontmatter block if present.
        """
        if not content.startswith("---"):
            return {}, content
            
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content
            
        try:
            metadata = yaml.safe_load(parts[1]) or {}
            return metadata, parts[2].strip()
        except Exception:
            return {}, content
