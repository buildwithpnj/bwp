import logging
from app.schemas.multimodal_input_schema import MultimodalInput
from app.schemas.normalized_signal_schema import NormalizedSignal
from app.services.ocr_processor import OcrProcessor
from app.services.image_processor import ImageProcessor
from app.services.document_processor import DocumentProcessor
from app.services.transcript_processor import TranscriptProcessor

logger = logging.getLogger("media_normalization_service")

class MediaNormalizationService:
    @classmethod
    def normalize(cls, input_data: MultimodalInput) -> NormalizedSignal:
        """
        Parses raw multimodal streams, extracts textual contents, runs safety gates,
        and translates outputs into NormalizedSignal objects.
        """
        media_type = input_data.media_type
        extracted = ""
        entities = {}
        intent_hints = []
        confidence = 0.95
        safety_flags = {"malicious_payload": False}
        suggested_wf = "generic_action"
        
        file_bytes = input_data.file_bytes or b""
        
        # 1. Processing Routing
        if media_type == "text":
            extracted = file_bytes.decode("utf-8", errors="ignore") if file_bytes else "Mock Text Input"
            intent_hints.append("text_input")
        elif media_type == "pdf" or media_type == "document":
            extracted = DocumentProcessor.extract_document_text(file_bytes)
            intent_hints.append("document_analysis")
            suggested_wf = "create_lesson_note"
        elif media_type == "screenshot" or media_type == "image":
            extracted = OcrProcessor.extract_ocr_text(file_bytes)
            img_details = ImageProcessor.process_image(file_bytes)
            entities["image_properties"] = img_details
            intent_hints.append("visual_ocr")
            suggested_wf = "build_practice_plan"
        elif media_type == "voice_transcript":
            extracted = TranscriptProcessor.process_voice_transcript(file_bytes)
            intent_hints.append("voice_command")
        else:
            extracted = "Fallback text content."
            confidence = 0.5
            
        # 2. Safety filter scan check
        extracted_lower = extracted.lower()
        if "drop table" in extracted_lower or "rm -rf" in extracted_lower or "malicious" in extracted_lower:
            logger.warning("Safety Scan: Potential injection payload intercepted.")
            safety_flags["malicious_payload"] = True
            confidence = 0.0
            
        return NormalizedSignal(
            media_type=media_type,
            extracted_text=extracted,
            detected_entities=entities,
            intent_hints=intent_hints,
            confidence=confidence,
            safety_flags=safety_flags,
            suggested_workflow_type=suggested_wf
        )
