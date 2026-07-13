import os
from typing import List

class KnowledgeDiscoveryService:
    @classmethod
    def discover_markdown_files(cls, directory_path: str) -> List[str]:
        """
        Discovers all Markdown files inside the target folder path recursively.
        """
        discovered = []
        if not os.path.exists(directory_path):
            return discovered
            
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".md"):
                    discovered.append(os.path.join(root, file))
        return discovered
