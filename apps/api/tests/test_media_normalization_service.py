import pytest
from app.services.media_normalization_service import MediaNormalizationService
from app.schemas.multimodal_input_schema import MultimodalInput

def test_media_normalization_types():
    # 1. Screenshot OCR Normalization
    req_screenshot = MultimodalInput(
        media_type="screenshot",
        raw_filename="snap.png",
        file_bytes=b"SettingsDrawer"
    )
    sig = MediaNormalizationService.normalize(req_screenshot)
    assert sig.media_type == "screenshot"
    assert "visual_ocr" in sig.intent_hints
    assert sig.suggested_workflow_type == "build_practice_plan"
    assert "image_properties" in sig.detected_entities
    
    # 2. Voice Transcript Normalization
    req_voice = MultimodalInput(
        media_type="voice_transcript",
        raw_filename="voice.wav",
        file_bytes=b"Resume workflow please."
    )
    sig_voice = MediaNormalizationService.normalize(req_voice)
    assert sig_voice.media_type == "voice_transcript"
    assert "voice_command" in sig_voice.intent_hints
    assert sig_voice.confidence == 0.95
