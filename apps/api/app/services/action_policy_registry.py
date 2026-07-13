from enum import Enum

class ActionPolicyTier(str, Enum):
    SAFE_AUTO = "safe_auto"
    CONFIRM_FIRST = "confirm_first"
    ADMIN_ONLY = "admin_only"
    DESTRUCTIVE_CONFIRMED = "destructive_confirmed"
    READ_ONLY = "read_only"

class ActionPolicyRegistry:
    # Policies mapping actions to policy tiers
    POLICIES = {
        # Notes
        "create_note": ActionPolicyTier.SAFE_AUTO,
        "update_note": ActionPolicyTier.SAFE_AUTO,
        "delete_note": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,
        "restore_note": ActionPolicyTier.SAFE_AUTO,
        "search_notes": ActionPolicyTier.READ_ONLY,

        # Tasks
        "create_task": ActionPolicyTier.SAFE_AUTO,
        "update_task": ActionPolicyTier.SAFE_AUTO,
        "complete_task": ActionPolicyTier.SAFE_AUTO,
        "prioritize_task": ActionPolicyTier.SAFE_AUTO,
        "delete_task": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,
        "restore_task": ActionPolicyTier.SAFE_AUTO,

        # Projects
        "create_project": ActionPolicyTier.SAFE_AUTO,
        "update_project": ActionPolicyTier.SAFE_AUTO,
        "complete_project": ActionPolicyTier.SAFE_AUTO,
        "delete_project": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Books
        "create_book": ActionPolicyTier.SAFE_AUTO,
        "update_book_progress": ActionPolicyTier.SAFE_AUTO,
        "archive_book": ActionPolicyTier.SAFE_AUTO,
        "delete_book": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Assets
        "create_asset": ActionPolicyTier.SAFE_AUTO,
        "update_asset": ActionPolicyTier.SAFE_AUTO,
        "delete_asset": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Media
        "upload_media_metadata": ActionPolicyTier.SAFE_AUTO,
        "update_media_metadata": ActionPolicyTier.SAFE_AUTO,
        "delete_media_metadata": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Storage
        "get_storage_status": ActionPolicyTier.READ_ONLY,
        "cleanup_storage": ActionPolicyTier.CONFIRM_FIRST,

        # Calendar
        "create_calendar_event": ActionPolicyTier.SAFE_AUTO,
        "update_calendar_event": ActionPolicyTier.SAFE_AUTO,
        "cancel_calendar_event": ActionPolicyTier.CONFIRM_FIRST,

        # Habits
        "create_habit": ActionPolicyTier.SAFE_AUTO,
        "log_habit_checkin": ActionPolicyTier.SAFE_AUTO,
        "delete_habit": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Quit Addiction
        "create_addiction_tracker": ActionPolicyTier.SAFE_AUTO,
        "log_addiction_relapse": ActionPolicyTier.SAFE_AUTO,
        "get_sobriety_stats": ActionPolicyTier.READ_ONLY,

        # Memory
        "create_memory_item": ActionPolicyTier.SAFE_AUTO,
        "update_memory_item": ActionPolicyTier.SAFE_AUTO,
        "delete_memory_item": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Knowledge
        "create_knowledge_item": ActionPolicyTier.SAFE_AUTO,
        "search_knowledge": ActionPolicyTier.READ_ONLY,
        "delete_knowledge_item": ActionPolicyTier.DESTRUCTIVE_CONFIRMED,

        # Mission Control
        "get_telemetry_status": ActionPolicyTier.READ_ONLY,
        "trigger_system_sync": ActionPolicyTier.ADMIN_ONLY,

        # Settings
        "update_preference": ActionPolicyTier.SAFE_AUTO,
        "update_reminder_preferences": ActionPolicyTier.SAFE_AUTO,

        # Trash
        "list_trash_items": ActionPolicyTier.READ_ONLY,
        "restore_trash_item": ActionPolicyTier.SAFE_AUTO,
        "permanent_purge_item": ActionPolicyTier.ADMIN_ONLY,

        # Test action mappings
        "fail_action": ActionPolicyTier.SAFE_AUTO,
    }

    @classmethod
    def get_policy(cls, action_name: str) -> ActionPolicyTier:
        return cls.POLICIES.get(action_name, ActionPolicyTier.CONFIRM_FIRST)
