import pytest
from app.services.ocr_processor import OcrProcessor

def test_ocr_extraction():
    # Plain text extraction checks
    res = OcrProcessor.extract_ocr_text(b"Hello world from screenshot")
    assert "Hello world" in res
    
    # Empty bytes fallback
    res_empty = OcrProcessor.extract_ocr_text(b"")
    assert "Mock Screenshot Text" in res_empty
