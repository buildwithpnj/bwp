import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.schemas.multimodal_input_schema import MultimodalInput
from app.models.multimodal_ingest_log import MultimodalIngestLog
from app.services.media_normalization_service import MediaNormalizationService
from app.services.signal_router import SignalRouter

logger = logging.getLogger("multimodal_ingestion_service")

class MultimodalIngestionService:
    @classmethod
    async def ingest_media(
        cls,
        db: AsyncSession,
        input_data: MultimodalInput
    ) -> Dict[str, Any]:
        """
        Orchestrates full multimodal pipeline: normalize inputs, save audit logs,
        check safety bounds, and route intents to workflows.
        """
        # 1. Normalize
        signal = MediaNormalizationService.normalize(input_data)
        
        # 2. Persist audit log
        log = MultimodalIngestLog(
            media_type=signal.media_type,
            raw_filename=input_data.raw_filename,
            extracted_text=signal.extracted_text,
            detected_entities=signal.detected_entities,
            safety_flags=signal.safety_flags,
            confidence=signal.confidence
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        
        # 3. Intercept unsafe safety flags
        if signal.safety_flags.get("malicious_payload"):
            logger.error("Ingestion Blocked: safety violation detected.")
            return {
                "status": "blocked",
                "message": "Security policy violation: potential injection threat flagged.",
                "ingest_log_id": log.id
            }
            
        # 4. Route signals to workflow planner
        wf_proposal = await SignalRouter.route_signal_to_workflow(db, signal)
        
        return {
            "status": "success",
            "ingest_log_id": log.id,
            "signal": signal.model_dump(),
            "workflow_proposal": wf_proposal
        }
