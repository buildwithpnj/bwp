import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.thread_context_link import ThreadContextLink

class ThreadContextAssembler:
    @classmethod
    async def link_entity_to_thread(
        cls,
        db: AsyncSession,
        thread_id: str,
        entity_type: str,
        entity_id: str
    ) -> ThreadContextLink:
        """
        Attaches a diagnostic workflow or objective loop context link to a thread.
        """
        link = ThreadContextLink(
            id=str(uuid.uuid4()),
            operating_thread_id=thread_id,
            linked_entity_type=entity_type,
            linked_entity_id=entity_id
        )
        db.add(link)
        await db.commit()
        return link
