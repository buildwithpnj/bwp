class ModalityGovernancePolicy:
    _max_file_sizes = {
        "text": 1048576,        # 1 MB
        "pdf": 15728640,        # 15 MB
        "screenshot": 5242880,  # 5 MB
        "voice_transcript": 2097152 # 2 MB
    }

    @classmethod
    def validate_file_size(cls, media_type: str, file_size_bytes: int) -> bool:
        """
        Validates file size ceilings for each modality.
        """
        limit = cls._max_file_sizes.get(media_type, 1048576)
        return file_size_bytes <= limit
