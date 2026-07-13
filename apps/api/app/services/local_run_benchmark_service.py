import time
import json
import os
import logging
from typing import Dict, Any, List
from app.services.llm_provider_router import LLMProviderRouter
from app.services.local_llm_metrics_service import LocalLlmMetricsService

logger = logging.getLogger("local_run_benchmark")

class LocalRunBenchmarkService:
    @classmethod
    async def run_benchmark_pass(cls) -> Dict[str, Any]:
        """
        Executes comparison eval set prompts and indexes metrics results.
        """
        eval_file = os.path.join(os.path.dirname(__file__), "..", "evals", "local_provider_comparison_eval_set.json")
        if not os.path.exists(eval_file):
            # Fallback inline config if eval file doesn't exist
            test_prompts = [
                {"id": "COMP-001", "prompt": "Identify typical oauth failures"},
                {"id": "COMP-002", "prompt": "Check my daily budget items"}
            ]
        else:
            try:
                with open(eval_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    test_prompts = data.get("test_cases", [])
            except Exception as e:
                logger.error(f"Failed to load benchmark evaluation dataset: {e}")
                test_prompts = []

        LocalLlmMetricsService.clear_metrics()
        results = []

        for case in test_prompts:
            prompt = case.get("prompt", "")
            case_id = case.get("id", "CASE-X")
            
            start_time = time.perf_counter()
            
            # Request completion
            response = await LLMProviderRouter.route_completion(
                messages=[{"role": "user", "content": prompt}],
                json_mode=False
            )
            
            end_time = time.perf_counter()
            latency = end_time - start_time
            
            success = response.get("status") == "success"
            usage = response.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            
            # Record metrics
            LocalLlmMetricsService.record_completion(
                latency=latency,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                status=response.get("status", "error"),
                fallback_triggered=(response.get("provider") == "cloud_fallback"),
                grounding_passed=success
            )

            results.append({
                "id": case_id,
                "prompt": prompt,
                "latency": latency,
                "success": success,
                "fallback_triggered": (response.get("provider") == "cloud_fallback"),
                "answer_preview": response.get("content", "")[:120]
            })

        summary = LocalLlmMetricsService.get_summary_metrics()
        return {
            "summary": summary,
            "results": results
        }
