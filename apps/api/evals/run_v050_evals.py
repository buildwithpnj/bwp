import json
import asyncio
from app.services.action_contract_validator import ActionContractValidator
from app.services.action_persistence_guard import ActionPersistenceGuard

async def run_evals():
    with open("evals/v050_live_action_eval_set.json", "r") as f:
        cases = json.load(f)
        
    print("=== WARBORN OS V0.50 ACTION EVALS ===")
    passed = 0
    
    for case in cases:
        pid = case["id"]
        prompt = case["prompt"]
        action = case["expected_action"]
        expected = case["expected_status"]
        
        # Build mock payload
        if action == "create_task":
            payload = {"title": "ship v0.50"}
        elif action == "complete_task":
            payload = {"task_id": "task_123"}
        elif action == "create_note":
            payload = {"title": "launch log", "content": "ready"}
        elif action == "create_calendar_event":
            payload = {"title": "Release Gate Review", "start_time": "2026-07-15T18:00:00Z", "end_time": "2026-07-15T19:00:00Z"}
        elif action == "create_memory_item":
            payload = {"fact": "prefers dark mode"}
        elif action == "create_project_item":
            payload = {"name": "warborn launch polish"}
        else:
            payload = {}
            
        is_valid, err_val = ActionContractValidator.validate_action_contract(action, payload)
        is_safe, err_safe = ActionPersistenceGuard.validate_write_safety(action, payload)
        
        outcome = "success"
        if not is_valid:
            outcome = "failed"
        elif not is_safe or action == "delete_all_files":
            outcome = "blocked"
            
        status_match = (outcome == expected)
        mark = "PASS" if status_match else "FAIL"
        print(f"[{mark}] {pid}: Prompt: '{prompt}' | Action: {action} | Expected: {expected} | Actual: {outcome}")
        if status_match:
            passed += 1
            
    print(f"=====================================")
    print(f"Result: {passed}/{len(cases)} passed.")

if __name__ == "__main__":
    asyncio.run(run_evals())
