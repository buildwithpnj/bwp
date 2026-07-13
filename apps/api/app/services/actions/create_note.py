import json
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.notes import Note

class CreateNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        content = payload["content"]
        
        note = Note(
            user_id=user_id,
            title=title,
            body_json=json.dumps({"text": content}),
            tags=""
        )
        db.add(note)
        await db.flush()
        
        return {
            "status": "success",
            "note_id": note.id,
            "message": f"Note '{title}' created successfully."
        }
