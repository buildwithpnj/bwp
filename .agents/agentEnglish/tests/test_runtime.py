import sys
import os
import pytest

# Put current directory on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runtime import classify_intent, run_agent
from schemas import AgentRequest

@pytest.mark.asyncio
async def test_intent_classification():
    # Correction intent
    assert await classify_intent("Can you correct my grammar?") == "english_correction"
    # Hinglish intent
    assert await classify_intent("What is meaning of please adjust?") == "hinglish_to_english"
    # Unallowed intent
    assert await classify_intent("Write a full python script for me") == "general"

@pytest.mark.asyncio
async def test_run_agent_preview_restriction():
    # Verify unallowed preview intent gets blocked
    req = AgentRequest(session_id="test_sess", message="Write code for a dashboard")
    res = await run_agent(req, is_preview=True)
    assert res.status_code if hasattr(res, "status_code") else res.status == "blocked"
    assert "preview scope" in res.message.lower()

@pytest.mark.asyncio
async def test_run_agent_allowed_preview():
    req = AgentRequest(session_id="test_sess", message="correct this: me goes to school")
    res = await run_agent(req, is_preview=True)
    assert res.status == "success"
    assert res.tokens_used > 0
