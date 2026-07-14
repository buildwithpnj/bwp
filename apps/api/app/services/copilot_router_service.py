import logging
from typing import Dict, Any, Tuple, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.copilot_context_payload import CopilotContextPayload
from app.services.page_context_service import PageContextService
from app.services.llm_provider_router import LLMProviderRouter
from app.services.hybrid_retrieval_service import HybridRetrievalService

logger = logging.getLogger("copilot_router_service")

# Route-specific system prompt expansions
_ROUTE_HINTS: Dict[str, str] = {
    "finance":   "The user is on the Finance page. You can help with budgets, transactions, account balances, and spending trends.",
    "habits":    "The user is on the Habits tracker. You can help with streak analysis, habit consistency, and goal planning.",
    "aicoach":   "The user is on the AI Coach page. You can help with personal development insights and learning recommendations.",
    "notes":     "The user is on the Notes page. You can help create, search, or summarise lesson notes and knowledge entries.",
    "books":     "The user is on the Books page. You can help track reading progress, summarise books, or recommend titles.",
    "recovery":  "The user is on the Recovery tracking page. You can help monitor sobriety streaks and wellness goals.",
    "dashboard": "The user is on the main dashboard. You can help navigate to any module, summarise their day, or answer general questions about Warborn OS.",
    "storage":   "The user is on the Storage page. You can help manage cloud drives and file syncing.",
}

_SYSTEM_PROMPT = """You are Warborn Copilot, an intelligent personal AI assistant embedded in Warborn OS — a personal productivity operating system.

You are context-aware: you know which page the user is on and can take relevant actions.
You are concise, helpful, and conversational. Respond naturally like a smart assistant, not a robot.
Never echo back the user's message verbatim. Always provide a real, useful response.
If the user's question references documents, knowledge, or their workspace data, use the provided Reference Data section to answer accurately.
If you don't know something or it is not in the reference data, say so honestly.
Keep replies under 3 sentences unless the user asks for detail.

If the user is asking to perform any dashboard operation (create, update, delete, archive, complete, restore, search, settings updates, etc. across notes, tasks, projects, books, habits, quit addiction, calendar, user memory, knowledge base, settings, etc.), you must output a special JSON action block inside <action>...</action> tags at the very end of your response.
Do NOT mention the action block to the user in your conversational reply.
The JSON inside the tags must follow this exact format:
{
  "action_name": "<action_name>",
  "payload": { ... }
}
All properties in the payload must strictly match the expected schemas (e.g. create_note requires 'title' and 'content'; log_habit_checkin requires 'habit_id' and 'date'; etc.).
"""


class CopilotRouterService:
    @classmethod
    async def process_query(
        cls,
        db: AsyncSession,
        query: str,
        ctx: CopilotContextPayload,
        user_id: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Sends query to LLM (via LLMProviderRouter) with full route context, retrieved RAG documents, and chat history.
        Returns (reply_text, suggested_action).
        """
        route = (ctx.current_route or "/dashboard").lower()

        # Build route-aware system prompt
        route_hint = ""
        for key, hint in _ROUTE_HINTS.items():
            if key in route:
                route_hint = hint
                break
        if not route_hint:
            route_hint = _ROUTE_HINTS["dashboard"]

        # 1. Retrieve relevant knowledge chunks matching user's query
        rag_context = ""
        try:
            chunks = await HybridRetrievalService.retrieve(db, user_id, query)
            if chunks:
                logger.info(f"Retrieved {len(chunks)} knowledge chunks for Copilot query: '{query}'")
                context_blocks = []
                for i, chunk in enumerate(chunks[:3]):  # Use top 3 matching chunks
                    text = chunk.get("chunk_text") or chunk.get("chunk_summary") or ""
                    context_blocks.append(f"[Document {i+1}]: {text}")
                rag_context = "\n\n".join(context_blocks)
        except Exception as e:
            logger.error(f"Failed to retrieve RAG knowledge chunks for user {user_id}: {e}")

        # Assemble prompt
        system_content = f"{_SYSTEM_PROMPT}\n\nCurrent context: {route_hint}"
        if rag_context:
            system_content += f"\n\nReference Data from User's Workspace:\n{rag_context}"

        from app.services.memory_injection_service import MemoryInjectionService
        system_content = await MemoryInjectionService.inject_memories_into_system_prompt(
            db=db,
            user_id=user_id,
            query=query,
            session_id=None,
            base_prompt=system_content
        )

        # Build message list: system + rolling history + current user message
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_content}]

        if history:
            # Include last 6 turns max to stay within context budget
            for entry in history[-6:]:
                role = entry.get("role", "user")
                content = entry.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": query})

        # Call LLM
        try:
            result = await LLMProviderRouter.route_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=512
            )

            if result.get("status") == "success":
                reply_text = result.get("content", "I'm not sure how to help with that.")
            else:
                logger.warning(f"LLM returned error: {result.get('message')}")
                reply_text = "I'm having trouble connecting to my AI brain right now. Please try again in a moment."

        except Exception as e:
            logger.error(f"CopilotRouterService LLM call failed: {e}")
            reply_text = "Something went wrong on my end. Please try again."

        # Detect structured actions from tags
        query_lower = query.lower()
        suggested_action: Dict[str, Any] = {}

        # Helper function to cleanse common payload mistakes by the LLM
        def cleanse_payload(action_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
            cleansed = {}
            if action_name == "create_task":
                cleansed["title"] = payload.get("title") or payload.get("name") or "New Task"
                cleansed["description"] = payload.get("description") or payload.get("notes") or payload.get("content") or payload.get("details")
                cleansed["category"] = payload.get("category") or payload.get("tag") or payload.get("type")
            elif action_name == "create_note":
                cleansed["title"] = payload.get("title") or payload.get("name") or "New Note"
                cleansed["content"] = payload.get("content") or payload.get("body") or payload.get("text") or "Empty Content"
                cleansed["tags"] = payload.get("tags")
            elif action_name == "create_project":
                cleansed["name"] = payload.get("name") or payload.get("title") or "New Project"
                cleansed["description"] = payload.get("description") or payload.get("notes") or payload.get("content")
            elif action_name == "create_book":
                cleansed["title"] = payload.get("title") or payload.get("name") or "Untitled Book"
                cleansed["author"] = payload.get("author") or payload.get("writer") or "Unknown"
                cleansed["status"] = payload.get("status") or "to-read"
            elif action_name == "create_calendar_event":
                from datetime import datetime, timedelta, timezone
                now_utc = datetime.now(timezone.utc)
                cleansed["title"] = payload.get("title") or payload.get("name") or "Calendar Event"
                cleansed["start_time"] = payload.get("start_time") or payload.get("start") or (now_utc + timedelta(hours=1)).isoformat()
                cleansed["end_time"] = payload.get("end_time") or payload.get("end") or (now_utc + timedelta(hours=2)).isoformat()
                cleansed["description"] = payload.get("description") or payload.get("notes") or payload.get("content")
            elif action_name == "create_habit":
                cleansed["name"] = payload.get("name") or payload.get("title") or "New Habit"
                cleansed["cadence"] = payload.get("cadence") or "daily"
                try:
                    cleansed["target"] = int(payload.get("target", 1))
                except Exception:
                    cleansed["target"] = 1
            elif action_name == "create_addiction_tracker":
                from datetime import datetime, timezone
                cleansed["name"] = payload.get("name") or payload.get("title") or "Recovery Tracker"
                cleansed["quit_date"] = payload.get("quit_date") or payload.get("date") or payload.get("start_date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
            else:
                # Fallback: copy keys as is
                cleansed = payload
            return {k: v for k, v in cleansed.items() if v is not None}

        # 1. Parse JSON inside <action>...</action> tags
        import re
        import json
        action_match = re.search(r"<action>(.*?)</action>", reply_text, re.DOTALL)
        
        if action_match:
            try:
                raw_json = action_match.group(1).strip()
                parsed = json.loads(raw_json)
                action_name = parsed.get("action_name")
                raw_payload = parsed.get("payload", {})
                
                # Apply parameter mapping and auto-correction
                cleansed_pay = cleanse_payload(action_name, raw_payload)
                
                # Validate using registry
                from app.services.copilot_action_registry import CopilotActionRegistry
                if CopilotActionRegistry.get_action(action_name) and CopilotActionRegistry.validate_inputs(action_name, cleansed_pay):
                    suggested_action = {
                        "action_name": action_name,
                        "payload": cleansed_pay
                    }
                # Always strip action tag from user-facing reply text to keep drawer UX clean
                reply_text = re.sub(r"<action>.*?</action>", "", reply_text, flags=re.DOTALL).strip()
            except Exception as e:
                logger.error(f"Failed to parse action tags: {e}")
                # Strip the tag even on parse errors so raw JSON is not dumped in chat
                reply_text = re.sub(r"<action>.*?</action>", "", reply_text, flags=re.DOTALL).strip()

        # 2. Fallback heuristics for note/task/habit/addiction/calendar actions
        if not suggested_action:
            has_create = any(w in query_lower for w in ["create", "add", "new", "save", "make", "write", "track"])
            
            # Note Fallback
            if has_create and any(w in query_lower for w in ["note", "notes", "memo"]):
                title = "Copilot Note"
                title_match = re.search(r"(?:named|titled|called)\s+([a-zA-Z0-9_\-\s]{1,50})", query, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                suggested_action = {
                    "action_name": "create_note",
                    "payload": {
                        "title": title,
                        "content": reply_text
                    }
                }
            # Task Fallback (Matches Quit Addiction Task or Regular Task)
            elif has_create and "task" in query_lower:
                title = "New Task"
                title_match = re.search(r"(?:task for|task named|task titled|task to|task)\s+([a-zA-Z0-9_\-\s]{1,50})", query, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip().capitalize()
                
                category = "general"
                if "addiction" in query_lower or "alcohol" in query_lower or "sobriety" in query_lower or "quit" in query_lower:
                    category = "recovery"
                
                suggested_action = {
                    "action_name": "create_task",
                    "payload": {
                        "title": title,
                        "description": f"Created via Copilot: {query}",
                        "category": category
                    }
                }
            # Addiction Tracker Fallback
            elif has_create and any(w in query_lower for w in ["addiction", "sobriety", "quit"]):
                from datetime import datetime, timezone
                name = "Recovery Tracker"
                name_match = re.search(r"(?:tracker for|tracker named|tracker to|quit|addiction)\s+([a-zA-Z0-9_\-\s]{1,50})", query, re.IGNORECASE)
                if name_match:
                    name = name_match.group(1).strip().capitalize()
                suggested_action = {
                    "action_name": "create_addiction_tracker",
                    "payload": {
                        "name": name,
                        "quit_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    }
                }
            # Habit Fallback
            elif has_create and "habit" in query_lower:
                name = "New Habit"
                name_match = re.search(r"(?:habit for|habit named|habit called|habit to|habit)\s+([a-zA-Z0-9_\-\s]{1,50})", query, re.IGNORECASE)
                if name_match:
                    name = name_match.group(1).strip().capitalize()
                suggested_action = {
                    "action_name": "create_habit",
                    "payload": {
                        "name": name,
                        "cadence": "daily",
                        "target": 1
                    }
                }
            # Navigation Fallback
            elif "navigate" in query_lower or "go to" in query_lower:
                target = "/dashboard"
                if "task" in query_lower:
                    target = "/tasks"
                elif "note" in query_lower:
                    target = "/notes"
                elif "habit" in query_lower:
                    target = "/habits"
                elif "book" in query_lower:
                    target = "/books"
                elif "recovery" in query_lower or "addiction" in query_lower:
                    target = "/recovery"
                elif "finance" in query_lower:
                    target = "/finance"
                suggested_action = {"action_name": "navigate_dashboard", "payload": {"target": target}}

        from app.services.copilot_persona_policy import CopilotPersonaPolicy
        reply_text = CopilotPersonaPolicy.scrub_planning_artifacts(reply_text)
        reply_text = CopilotPersonaPolicy.sanitize_reply(reply_text)

        return reply_text, suggested_action

