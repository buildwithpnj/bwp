import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.models.notes import Note

class UpdateNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        note_id = payload["note_id"]
        title = payload["title"]
        content = payload["content"]
        
        stmt = select(Note).where(Note.id == note_id, Note.user_id == user_id)
        res = await db.execute(stmt)
        note = res.scalar_one_or_none()
        
        if not note:
            return {"status": "failed", "error": "Note not found or unauthorized access."}
            
        note.title = title
        note.body_json = json.dumps({"text": content})
        db.add(note)
        await db.flush()
        
        return {
            "status": "success",
            "note_id": note.id,
            "message": f"Note '{title}' updated successfully."
        }
