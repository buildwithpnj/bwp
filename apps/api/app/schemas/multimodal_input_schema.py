from pydantic import BaseModel, Field
from typing import Optional

class MultimodalInput(BaseModel):
    media_type: str = Field(..., description="Modality type: text, pdf, screenshot, voice_transcript")
    raw_filename: str = Field(..., description="File identifier or name.")
    file_bytes: Optional[bytes] = Field(None, description="Raw file attachment content bytes.")
