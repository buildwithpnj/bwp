import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.context_compaction_run import ContextCompactionRun
from app.services.workflow_trace_compactor import WorkflowTraceCompactor

class MemoryCompactionService:
    @classmethod
    async def compact_memory(
        cls,
        db: AsyncSession,
        user_id: str,
        raw_traces: list
    ) -> str:
        """
        Compresses older workflow logs to minimize prompt size while retaining key details.
        """
        raw_tokens = len(str(raw_traces)) * 4
        compacted = WorkflowTraceCompactor.compact_traces(raw_traces)
        comp_tokens = len(compacted) * 4
        
        ratio = 1.0 - (comp_tokens / max(raw_tokens, 1))
        
        # Log run
        run = ContextCompactionRun(
            id=str(uuid.uuid4()),
            user_id=user_id,
            raw_tokens_count=raw_tokens,
            compacted_tokens_count=comp_tokens,
            reduction_ratio=ratio
        )
        db.add(run)
        await db.commit()
        
        return compacted
