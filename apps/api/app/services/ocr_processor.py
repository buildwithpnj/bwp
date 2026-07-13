class OcrProcessor:
    @classmethod
    def extract_ocr_text(cls, file_bytes: bytes) -> str:
        """
        Simulates OCR text extraction from raw image or screenshot data bytes.
        """
        if not file_bytes:
            return "Mock Screenshot Text: User opened the dashboard settings panel."
        try:
            # Simply decode to check string or return mock content
            text = file_bytes.decode("utf-8", errors="ignore")
            if len(text.strip()) > 5:
                return text
        except Exception:
            pass
        return "Mock OCR Text: Focus focus focus, master grammar patterns."
