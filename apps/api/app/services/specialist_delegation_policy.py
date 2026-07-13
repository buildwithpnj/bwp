import logging
from typing import Dict, Any
from app.services.subagent_registry import SubAgentRegistry

logger = logging.getLogger("specialist_delegation_policy")

class SpecialistDelegationPolicy:
    # Track simulated session token usage
    _token_spent: float = 0.0
    # Track recursion depth
    _delegation_depth: int = 0
    _max_recursion_depth: int = 2

    @classmethod
    def validate_delegation(cls, specialist_type: str, domain: str) -> bool:
        """
        Enforces policy limits on subagent triggers, protecting budget and loop bounds.
        """
        specialist = SubAgentRegistry.get_specialist(specialist_type)
        if not specialist:
            logger.warning(f"Policy Block: Specialist '{specialist_type}' not registered.")
            return False
            
        # 1. Domain verification check
        if domain not in specialist.allowed_input_domains:
            logger.warning(f"Policy Block: Domain '{domain}' not in specialist '{specialist_type}' bounds.")
            return False
            
        # 2. Token budget check
        if cls._token_spent >= 15.0:
            logger.warning("Policy Block: Session token budget cap reached.")
            return False
            
        # 3. Recursion depth check
        if cls._delegation_depth >= cls._max_recursion_depth:
            logger.warning("Policy Block: Recursive delegation depth exceeded.")
            return False
            
        return True

    @classmethod
    def increment_counters(cls, tokens: float) -> None:
        cls._token_spent += tokens
        cls._delegation_depth += 1

    @classmethod
    def reset_policy_limits(cls) -> None:
        cls._token_spent = 0.0
        cls._delegation_depth = 0
