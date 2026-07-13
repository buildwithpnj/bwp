from typing import Dict, Any, Tuple
from app.schemas.copilot_context_payload import CopilotContextPayload
from app.services.page_context_service import PageContextService

class CopilotRouterService:
    @classmethod
    def process_query(
        cls,
        query: str,
        ctx: CopilotContextPayload
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Interprets chat query and determines if it triggers navigation or action suggestions.
        """
        query_lower = query.lower()
        explanation = PageContextService.get_route_explanation(ctx)
        
        suggested_action = {}
        response_text = f"Explanation: {explanation}. Understood message: '{query}'."
        
        if "create" in query_lower or "note" in query_lower:
            suggested_action = {
                "action_name": "create_lesson_note",
                "payload": {"title": "Copilot Note", "content": "Created via Copilot chat."}
            }
            response_text += " Suggested action: Create Lesson Note."
            
        elif "navigate" in query_lower:
            response_text = "Redirecting viewport to Dashboard visual analytics node."
            suggested_action = {"action_name": "navigate_dashboard", "payload": {"target": "/dashboard"}}
            
        return response_text, suggested_action
