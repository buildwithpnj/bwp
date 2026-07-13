from app.schemas.copilot_context_payload import CopilotContextPayload

class PageContextService:
    @classmethod
    def get_route_explanation(cls, ctx: CopilotContextPayload) -> str:
        """
        Explains dashboard elements based on the injected context route.
        """
        route = ctx.current_route.lower()
        if "finance" in route:
            return "You are viewing the Finance portal. It displays monthly accounts, transactions, and budgets."
        if "habits" in route:
            return "You are viewing the Habits tracker page showing daily consistency logs."
        if "aicoach" in route:
            return "You are viewing AI Coach insights for personal development."
        return "You are browsing the main Personal OS workspace dashboard."
