from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.schemas.normalized_signal_schema import NormalizedSignal

class SignalRouter:
    @classmethod
    async def route_signal_to_workflow(
        cls,
        db: AsyncSession,
        signal: NormalizedSignal
    ) -> Dict[str, Any]:
        """
        Translates normalized modality signals into workflow task blueprints.
        """
        wf_type = signal.suggested_workflow_type
        
        steps = []
        requires_approval = True
        
        if wf_type == "create_lesson_note":
            steps.append({
                "action_name": "create_lesson_note",
                "payload": {"title": "Modality Note Extraction", "content": signal.extracted_text}
            })
            requires_approval = False
        elif wf_type == "build_practice_plan":
            steps.append({
                "action_name": "build_practice_plan",
                "payload": {"focus_area": "grammar", "num_tasks": 3}
            })
            requires_approval = True
        else:
            steps.append({
                "action_name": "create_summary_note",
                "payload": {"summary": signal.extracted_text}
            })
            requires_approval = False
            
        return {
            "suggested_workflow_type": wf_type,
            "requires_approval": requires_approval,
            "steps": steps,
            "goal": f"Execute action prompted by {signal.media_type} ingestion pipeline."
        }
