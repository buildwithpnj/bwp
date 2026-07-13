class PageIntentClassifier:
    @classmethod
    def classify_intent(cls, route: str) -> str:
        """
        Classifies UI pages into intents to determine copilot talkativeness.
        """
        lower = route.lower()
        if "diagnostics" in lower or "recovery" in lower:
            return "stuck"
        elif "workspace" in lower or "tools" in lower:
            return "executing"
        elif "objectives" in lower:
            return "reviewing"
        return "browsing"
