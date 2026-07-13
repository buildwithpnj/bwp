class PreventiveNotificationService:
    @classmethod
    def format_alert(cls, risk_score: float, scope: str) -> str:
        """
        Builds proactive warning warnings description text.
        """
        return f"[Observability Warning] Rising failure pattern risk indices ({int(risk_score * 100)}%) detected in scope {scope}."
