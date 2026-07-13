import os

files_to_clean = [
    "app/routers/release_control_router.py",
    "app/schemas/rollout_decision_schema.py",
    "app/services/canary_rollout_service.py",
    "app/services/canary_scope_selector.py",
    "app/services/federated_rollback_service.py",
    "app/services/release_approval_service.py",
    "app/services/release_gate_service.py",
    "app/services/release_plan_validator.py",
    "app/services/release_safety_score_service.py",
    "app/services/rollback_bundle_builder.py",
    "app/services/rollback_preview_service.py",
    "app/services/rollback_trigger_service.py",
    "app/services/rollout_health_service.py",
    "app/services/rollout_stage_manager.py",
    "tests/test_canary_rollout_service.py",
    "tests/test_release_control_router.py",
    "tests/test_release_gate_service.py",
    "tests/test_release_plan_validator.py",
    "tests/test_rollback_trigger_service.py",
    "tests/test_rollout_health_service.py"
]

base_dir = r"c:\Users\praka\OneDrive\Documents\My dashboard\apps\api"

for f in files_to_clean:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Remove the MaroonColor line
        lines = content.splitlines()
        new_lines = [l for l in lines if "MaroonColor" not in l]
        new_content = "\n".join(new_lines) + "\n"
        
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Cleaned: {f}")
