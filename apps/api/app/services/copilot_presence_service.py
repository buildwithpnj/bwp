from app.services.page_intent_classifier import PageIntentClassifier
from app.services.copilot_prompt_policy import CopilotPromptPolicy

class CopilotPresenceService:
    @classmethod
    def evaluate_presence(cls, route: str, risk_tier: str = "low") -> dict:
        """
        Orchestrates route checks to configure copilot visual modes.
        """
        intent = PageIntentClassifier.classify_intent(route)
        directive = CopilotPromptPolicy.get_interaction_directive(intent, risk_tier)
        
        return {
            "intent": intent,
            "directive": directive,
            "should_show_hint": directive != "stay_silent"
        }
