class LoopCostTracker:
    @classmethod
    def calculate_cost(cls, prompt_tokens: int, completion_tokens: int, model: str = "gpt-3.5-turbo") -> float:
        """
        Calculates financial cost of the loop execution tokens.
        """
        # Pricing per 1000 tokens
        rates = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gemini-2.0-flash": {"input": 0.00015, "output": 0.0006},
            "ollama": {"input": 0.0, "output": 0.0} # Local is free!
        }
        
        # Determine rates
        rate = rates.get("gpt-3.5-turbo")
        for key, value in rates.items():
            if key in model.lower():
                rate = value
                break
                
        cost = ((prompt_tokens / 1000) * rate["input"]) + ((completion_tokens / 1000) * rate["output"])
        return round(cost, 6)
