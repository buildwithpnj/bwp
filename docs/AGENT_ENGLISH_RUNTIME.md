# Agent English Runtime

The `agentEnglish` module resides in `.agents/agentEnglish` and acts as the core LLM execution pipeline.

## Module Structure

* `runtime.py`: Main entry point for executing prompt pipelines. Exposes `async def run_agent(request: AgentRequest, is_preview: bool = False) -> AgentResponse`.
* `config.py`: Contains session constraints, default model identifiers (`gpt-4o-mini`), and rate limit structures.
* `schemas.py`: Strongly-typed input and output shapes using Pydantic models.
* `prompts/`: Store core templates, separating prompt text from orchestrator structures.

## Runtime Parameters
1. `is_preview=True`: Enforces the preview constraints, running prompt-intent classification.
2. `is_preview=False`: Executes unrestricted requests, allowing connection to persistent tools, memory, and database writes.
