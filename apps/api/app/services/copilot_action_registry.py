from typing import Dict, Any, List, Optional
from app.services.action_policy_registry import ActionPolicyRegistry, ActionPolicyTier
from app.services.action_schema_registry import SCHEMA_MAP

class CopilotActionRegistry:
    # Centrally defined dictionary of all dashboard control actions
    # Total actions: 56 actions across 15 modules
    ACTIONS = {
        # Notes (5 actions)
        "create_note": {
            "description": "Creates a new workspace note.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },
        "update_note": {
            "description": "Updates an existing note's title, tags, or content.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },
        "delete_note": {
            "description": "Deletes a note (moves to trash).",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },
        "restore_note": {
            "description": "Restores a note from trash.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },
        "search_notes": {
            "description": "Searches existing notes by query.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },

        # Tasks (6 actions)
        "create_task": {
            "description": "Creates a new operational task.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },
        "update_task": {
            "description": "Updates task status and progress.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },
        "complete_task": {
            "description": "Marks a task as completed.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },
        "prioritize_task": {
            "description": "Pins or prioritizes a task.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },
        "delete_task": {
            "description": "Deletes a task (moves to trash).",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },
        "restore_task": {
            "description": "Restores a task from trash.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },

        # Projects (4 actions)
        "create_project": {
            "description": "Creates a new project item tracking entry.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "projects",
        },
        "update_project": {
            "description": "Updates a project item's status, name, or description.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "projects",
        },
        "complete_project": {
            "description": "Marks a project as completed.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "projects",
        },
        "delete_project": {
            "description": "Deletes a project item (moves to trash).",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "projects",
        },

        # Books (4 actions)
        "create_book": {
            "description": "Adds a book to the readings list.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "books",
        },
        "update_book_progress": {
            "description": "Updates book progress, status, or rating.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "books",
        },
        "archive_book": {
            "description": "Archives a book from active reading list.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "books",
        },
        "delete_book": {
            "description": "Deletes a book (moves to trash).",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "books",
        },

        # Assets (3 actions)
        "create_asset": {
            "description": "Creates an asset tracking record.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "assets",
        },
        "update_asset": {
            "description": "Updates asset information.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "assets",
        },
        "delete_asset": {
            "description": "Deletes an asset record.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "assets",
        },

        # Media (3 actions)
        "upload_media_metadata": {
            "description": "Uploads metadata for media resources.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "media",
        },
        "update_media_metadata": {
            "description": "Updates media title or tags.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "media",
        },
        "delete_media_metadata": {
            "description": "Deletes media metadata record.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "media",
        },

        # Storage (2 actions)
        "get_storage_status": {
            "description": "Retrieves the storage usage and limits.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "storage",
        },
        "cleanup_storage": {
            "description": "Cleans up storage cache older than N days.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "storage",
        },

        # Calendar (3 actions)
        "create_calendar_event": {
            "description": "Creates a new calendar event entry.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "calendar",
        },
        "update_calendar_event": {
            "description": "Updates an existing calendar event title or timings.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "calendar",
        },
        "cancel_calendar_event": {
            "description": "Cancels a calendar event.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "calendar",
        },

        # Habits (3 actions)
        "create_habit": {
            "description": "Creates a new habit routine.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "habits",
        },
        "log_habit_checkin": {
            "description": "Logs habit completions or progressive values.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "habits",
        },
        "delete_habit": {
            "description": "Deletes a habit tracker.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "habits",
        },

        # Quit Addiction (3 actions)
        "create_addiction_tracker": {
            "description": "Initiates sobriety timer for an addiction.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "quit_addiction",
        },
        "log_addiction_relapse": {
            "description": "Records relapse date and resetssobriety timer.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "quit_addiction",
        },
        "get_sobriety_stats": {
            "description": "Retrieves statistics for sobriety trackers.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "quit_addiction",
        },

        # Memory (3 actions)
        "create_memory_item": {
            "description": "Adds fact or trait to user memory.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "memory",
        },
        "update_memory_item": {
            "description": "Updates user memory preferences.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "memory",
        },
        "delete_memory_item": {
            "description": "Removes a specific memory item.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "memory",
        },

        # Knowledge (3 actions)
        "create_knowledge_item": {
            "description": "Saves a fact or article in the knowledge base.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "knowledge",
        },
        "search_knowledge": {
            "description": "Searches the workspace knowledge base.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "knowledge",
        },
        "delete_knowledge_item": {
            "description": "Deletes a knowledge base item.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "knowledge",
        },

        # Mission Control (2 actions)
        "get_telemetry_status": {
            "description": "Queries central server telemetry status.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "mission_control",
        },
        "trigger_system_sync": {
            "description": "Triggers administrative system telemetry synchronization.",
            "allowed_roles": ["internal_admin"],
            "module": "mission_control",
        },

        # Settings (3 actions)
        "update_preference": {
            "description": "Updates workspace response mode and tone settings.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "settings",
        },
        "update_reminder_preferences": {
            "description": "Customizes notification and alert settings.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "settings",
        },
        "update_settings_preference": {
            "description": "Updates sensitive workspace settings and parameters.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "settings",
        },

        # Trash (5 actions)
        "list_trash_items": {
            "description": "Lists all deleted items in the trash bin.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "trash",
        },
        "restore_trash_item": {
            "description": "Restores a soft-deleted item back to active.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "trash",
        },
        "permanent_purge_item": {
            "description": "Purges an item permanently from databases.",
            "allowed_roles": ["internal_admin"],
            "module": "trash",
        },
        "permanently_delete_item": {
            "description": "Permanently deletes an item from trash, bypassing standard restore.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "trash",
        },
        "purge_trash": {
            "description": "Purges all soft-deleted items currently in the trash bin.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "trash",
        },

        # Notes additional (1 action)
        "archive_note": {
            "description": "Archives a workspace note card.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "notes",
        },

        # Tasks additional (1 action)
        "move_task_to_project": {
            "description": "Moves a task to a designated project.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "tasks",
        },

        # System telemetry / agent metadata (2 actions)
        "get_recent_updates": {
            "description": "Retrieves recent changes across all active workspace records.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "mission_control",
        },
        "get_agent_status": {
            "description": "Checks the operational status of the Copilot background process.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "module": "mission_control",
        },

        # Privileged actions (4 actions)
        "reveal_sensitive_config": {
            "description": "Exposes encrypted configuration blocks or sensitive variables.",
            "allowed_roles": ["internal_admin"],
            "module": "settings",
        },
        "delete_shared_workspace_resources": {
            "description": "Deletes core database assets shared across workspace users.",
            "allowed_roles": ["internal_admin"],
            "module": "projects",
        },
        "modify_system_policies": {
            "description": "Modifies base access-control or execution policies.",
            "allowed_roles": ["internal_admin"],
            "module": "settings",
        },
        "access_restricted_credentials": {
            "description": "Requests plaintext API keys or credentials.",
            "allowed_roles": ["internal_admin"],
            "module": "settings",
        },
    }

    @classmethod
    def get_action(cls, action_name: str) -> Optional[Dict[str, Any]]:
        action = cls.ACTIONS.get(action_name)
        if not action:
            return None
            
        policy = ActionPolicyRegistry.get_policy(action_name)
        schema = SCHEMA_MAP.get(action_name)
        
        return {
            **action,
            "policy_tier": policy,
            "input_schema": schema,
            "requires_approval": policy in [ActionPolicyTier.CONFIRM_FIRST, ActionPolicyTier.DESTRUCTIVE_CONFIRMED]
        }

    @classmethod
    def list_actions(cls) -> List[str]:
        return list(cls.ACTIONS.keys())

    @classmethod
    def validate_inputs(cls, action_name: str, payload: Dict[str, Any]) -> bool:
        schema_cls = SCHEMA_MAP.get(action_name)
        if not schema_cls:
            return False
        try:
            schema_cls(**payload)
            return True
        except Exception:
            return False
