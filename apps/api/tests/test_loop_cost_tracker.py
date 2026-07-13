import pytest
from app.services.loop_cost_tracker import LoopCostTracker

def test_loop_cost_tracker():
    cost_gpt4o = LoopCostTracker.calculate_cost(1000, 1000, "gpt-4o")
    assert cost_gpt4o == 0.02 # (1.0 * 0.005) + (1.0 * 0.015)
    
    cost_local = LoopCostTracker.calculate_cost(1000, 1000, "ollama")
    assert cost_local == 0.0
