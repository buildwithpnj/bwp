import json
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.notes import Note

class CreateLessonNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a structured learning note card in user dashboard notebook."""
        title = payload["title"]
        content = payload["content"]
        
        # Save note metadata in app models
        note = Note(
            user_id=user_id,
            title=title,
            body_json=json.dumps({"text": content}),
            tags=""
        )
        db.add(note)
        await db.flush()  # Populates note.id without final transaction commit yet
        
        return {
            "status": "success",
            "note_id": note.id,
            "message": f"Successfully created lesson note: '{title}'"
        }
