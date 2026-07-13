import pytest
from unittest.mock import AsyncMock
from app.services.resilience_policy_service import ResiliencePolicyService
from app.schemas.resilience_policy_schema import ResiliencePolicyCreate
from app.services.degraded_mode_manager import DegradedModeManager
from app.services.provider_health_guard import ProviderHealthGuard
from app.services.fallback_routing_service import FallbackRoutingService
from app.services.recovery_transition_service import RecoveryTransitionService

@pytest.mark.asyncio
async def test_resilience_self_healing():
    db = AsyncMock()
    
    # 1. Register Policy
    req = ResiliencePolicyCreate(
        trigger_type="openai_outage",
        affected_scope="chat_copilot",
        degradation_level="degraded",
        token_budget_reduction_factor=0.5
    )
    policy = await ResiliencePolicyService.configure_policy(db, req)
    assert policy.trigger_type == "openai_outage"
    
    # 2. Provider Health Check
    assert ProviderHealthGuard.evaluate_provider_health(0.3, 200.0) == "critical"
    assert ProviderHealthGuard.evaluate_provider_health(0.02, 100.0) == "healthy"
    
    # 3. Fallback Route resolution
    assert FallbackRoutingService.get_fallback_provider("openai", "critical") == "ollama_local"
    assert FallbackRoutingService.get_fallback_provider("openai", "degraded") == "gpt-4o-mini"
    
    # 4. Activate degraded operations & Transitions
    act = await DegradedModeManager.activate_degraded(db, "chat_copilot", "cached_summaries", "voice_audio")
    assert act.affected_scope == "chat_copilot"
    
    rec = await RecoveryTransitionService.log_recovery(db, "chat_copilot")
    assert rec.recovery_status == "completed"
