class CopilotPromptPolicy:
    @classmethod
    def get_interaction_directive(cls, user_intent: str, risk_tier: str = "low") -> str:
        """
        Determines the copilot talkativeness directive based on user status and risks.
        """
        if risk_tier == "high":
            return "stay_silent"
            
        if user_intent == "stuck":
            return "suggest_recovery"
        elif user_intent == "executing":
            return "stay_silent"
        elif user_intent == "reviewing":
            return "summarize"
        return "ask_open_ended"
