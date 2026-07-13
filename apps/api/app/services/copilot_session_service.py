import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, List, Optional
from app.models.copilot_session import CopilotSession
from app.schemas.copilot_message import CopilotMessage

class CopilotSessionService:
    @classmethod
    async def get_or_create_session(cls, db: AsyncSession, user_id: str) -> CopilotSession:
        """
        Retrieves active copilot session or provisions a new one.
        """
        stmt = select(CopilotSession).where(
            CopilotSession.user_id == user_id,
            CopilotSession.is_active == True
        )
        res = await db.execute(stmt)
        sess = res.scalar_one_or_none()
        
        if not sess:
            sess = CopilotSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                chat_history=[],
                is_active=True
            )
            db.add(sess)
            await db.commit()
            await db.refresh(sess)
        return sess

    @classmethod
    async def append_message(
        cls,
        db: AsyncSession,
        sess: CopilotSession,
        role: str,
        content: str,
        suggested_action: Optional[Dict[str, Any]] = None
    ) -> CopilotSession:
        """
        Appends message history.
        """
        history = list(sess.chat_history)
        history.append({
            "role": role,
            "content": content,
            "suggested_action": suggested_action
        })
        sess.chat_history = history
        db.add(sess)
        await db.commit()
        await db.refresh(sess)
        return sess
