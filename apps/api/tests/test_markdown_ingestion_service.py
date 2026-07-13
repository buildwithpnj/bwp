import pytest
import os
from unittest.mock import AsyncMock
from app.services.frontmatter_parser import FrontmatterParser
from app.services.document_cleaning_service import DocumentCleaningService
from app.services.knowledge_hash_service import KnowledgeHashService
from app.services.knowledge_discovery_service import KnowledgeDiscoveryService

def test_markdown_parsing_and_cleaning():
    # 1. Frontmatter parser
    raw = "---\ntitle: Governance Policy\nslug: gov_policy\n---\n# Header\nHello World"
    metadata, body = FrontmatterParser.parse_content(raw)
    assert metadata["title"] == "Governance Policy"
    assert "# Header" in body
    
    # 2. Text cleaning normalizer
    assert DocumentCleaningService.clean_text("  hello    world  \n") == "hello world"
    
    # 3. Hash verification
    h1 = KnowledgeHashService.compute_hash("hello")
    h2 = KnowledgeHashService.compute_hash("hello")
    assert h1 == h2
    
    # 4. File discovery
    files = KnowledgeDiscoveryService.discover_markdown_files("invalid_folder_path")
    assert len(files) == 0
