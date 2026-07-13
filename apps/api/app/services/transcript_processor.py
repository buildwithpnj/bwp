class TranscriptProcessor:
    @classmethod
    def process_voice_transcript(cls, file_bytes: bytes) -> str:
        """
        Simulates voice transcription / speech-to-text processing.
        """
        if not file_bytes:
            return "Voice Command: Resume the current failed workflow step."
        return file_bytes.decode("utf-8", errors="ignore")
