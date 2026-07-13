from fastapi import APIRouter, status, HTTPException
from typing import Dict, Any
from app.deps import CurrentUser
from app.services.local_model_health_service import LocalModelHealthService
from app.services.local_llm_metrics_service import LocalLlmMetricsService
from app.services.local_run_benchmark_service import LocalRunBenchmarkService
from app.services.local_loop_runtime import LocalLoopRuntime

router = APIRouter(prefix="/api/llm", tags=["Local LLM Diagnostics Plane"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def get_llm_health(current_user: CurrentUser):
    """
    Checks status of local inference servers.
    """
    return await LocalModelHealthService.check_health()

@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_llm_metrics(current_user: CurrentUser):
    """
    Retrieves performance and quality analytics.
    """
    return LocalLlmMetricsService.get_summary_metrics()

@router.post("/benchmark", status_code=status.HTTP_200_OK)
async def run_llm_benchmark(current_user: CurrentUser):
    """
    Runs active benchmark sets.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires administrator privileges."
        )
    return await LocalRunBenchmarkService.run_benchmark_pass()

@router.post("/loop-test", status_code=status.HTTP_200_OK)
async def run_loop_test(prompt: str, current_user: CurrentUser):
    """
    Runs multi-step RAG loop with actions disabled.
    """
    return await LocalLoopRuntime.execute_local_loop(prompt=prompt)

@router.get("/config", status_code=status.HTTP_200_OK)
async def get_llm_config(current_user: CurrentUser):
    """
    Returns the loaded LLM settings.
    """
    from app.llm_settings import llm_settings
    return {
        "llm_provider": llm_settings.llm_provider,
        "local_ai_enabled": llm_settings.local_ai_enabled,
        "ollama_base_url": llm_settings.ollama_base_url,
        "ollama_model": llm_settings.ollama_model,
        "primary_cloud_provider": llm_settings.primary_cloud_provider
    }

