from pydantic import BaseModel, Field
from typing import Optional, List

# Note schemas
class CreateNoteInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    tags: Optional[str] = None

class UpdateNoteInput(BaseModel):
    note_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

class DeleteNoteInput(BaseModel):
    note_id: str

class RestoreNoteInput(BaseModel):
    note_id: str

class SearchNotesInput(BaseModel):
    query: str

# Task schemas
class CreateTaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None

class UpdateTaskInput(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None

class CompleteTaskInput(BaseModel):
    task_id: str

class PrioritizeTaskInput(BaseModel):
    task_id: str
    pinned: bool

class DeleteTaskInput(BaseModel):
    task_id: str

class RestoreTaskInput(BaseModel):
    task_id: str

# Project schemas
class CreateProjectInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class UpdateProjectInput(BaseModel):
    project_id: str
    status: str
    name: Optional[str] = None
    description: Optional[str] = None

class CompleteProjectInput(BaseModel):
    project_id: str

class DeleteProjectInput(BaseModel):
    project_id: str

# Book schemas
class CreateBookInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    status: Optional[str] = "to-read"

class UpdateBookProgressInput(BaseModel):
    book_id: str
    status: str
    rating: Optional[int] = None

class ArchiveBookInput(BaseModel):
    book_id: str

class DeleteBookInput(BaseModel):
    book_id: str

# Asset schemas
class CreateAssetInput(BaseModel):
    name: str
    provider: str
    bucket: str

class UpdateAssetInput(BaseModel):
    asset_id: str
    name: str

class DeleteAssetInput(BaseModel):
    asset_id: str

# Media schemas
class UploadMediaMetadataInput(BaseModel):
    title: str
    file_path: str

class UpdateMediaMetadataInput(BaseModel):
    media_id: str
    title: str

class DeleteMediaMetadataInput(BaseModel):
    media_id: str

# Storage schemas
class GetStorageStatusInput(BaseModel):
    pass

class CleanupStorageInput(BaseModel):
    days_old: int

# Calendar schemas
class CreateCalendarEventInput(BaseModel):
    title: str = Field(..., min_length=1)
    start_time: str
    end_time: str
    description: Optional[str] = None

class UpdateCalendarEventInput(BaseModel):
    event_id: str
    title: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class CancelCalendarEventInput(BaseModel):
    event_id: str

# Habit schemas
class CreateHabitInput(BaseModel):
    name: str = Field(..., min_length=1)
    cadence: str = "daily"
    target: int = 1

class LogHabitCheckinInput(BaseModel):
    habit_id: str
    date: str
    value: Optional[float] = 1.0

class DeleteHabitInput(BaseModel):
    habit_id: str

# Quit Addiction schemas
class CreateAddictionTrackerInput(BaseModel):
    name: str
    quit_date: str

class LogAddictionRelapseInput(BaseModel):
    tracker_id: str
    relapse_date: str

class GetSobrietyStatsInput(BaseModel):
    tracker_id: str

# Memory schemas
class CreateMemoryItemInput(BaseModel):
    fact: str

class UpdateMemoryItemInput(BaseModel):
    tone: Optional[str] = None
    explanation_style: Optional[str] = None

class DeleteMemoryItemInput(BaseModel):
    fact: str

# Knowledge schemas
class CreateKnowledgeItemInput(BaseModel):
    title: str
    content: str

class SearchKnowledgeInput(BaseModel):
    query: str

class DeleteKnowledgeItemInput(BaseModel):
    item_id: str

# Mission Control schemas
class GetTelemetryStatusInput(BaseModel):
    pass

class TriggerSystemSyncInput(BaseModel):
    pass

# Settings schemas
class UpdatePreferenceInput(BaseModel):
    tone: str
    explanation_style: str

class UpdateReminderPreferencesInput(BaseModel):
    frequency: str

# Trash schemas
class ListTrashItemsInput(BaseModel):
    pass

class RestoreTrashItemInput(BaseModel):
    item_type: str
    item_id: str

class PermanentPurgeItemInput(BaseModel):
    item_type: str
    item_id: str

# New inputs for v0.50.1 Action Layer
class GetRecentUpdatesInput(BaseModel):
    limit: Optional[int] = 10

class GetAgentStatusInput(BaseModel):
    agent_id: Optional[str] = None

class MoveTaskToProjectInput(BaseModel):
    task_id: str
    project_id: str

class UpdateSettingsPreferenceInput(BaseModel):
    key: str
    value: str

class PermanentlyDeleteItemInput(BaseModel):
    item_type: str
    item_id: str

class PurgeTrashInput(BaseModel):
    confirm: bool = True

class RevealSensitiveConfigInput(BaseModel):
    config_key: str

class DeleteSharedWorkspaceResourcesInput(BaseModel):
    resource_id: str

class ModifySystemPoliciesInput(BaseModel):
    policy_name: str
    enabled: bool

class AccessRestrictedCredentialsInput(BaseModel):
    credential_name: str

# Central Map of Schemas
SCHEMA_MAP = {
    # Notes
    "create_note": CreateNoteInput,
    "update_note": UpdateNoteInput,
    "delete_note": DeleteNoteInput,
    "restore_note": RestoreNoteInput,
    "search_notes": SearchNotesInput,
    "archive_note": DeleteNoteInput,  # maps to note deletion schema for simplicity

    # Tasks
    "create_task": CreateTaskInput,
    "update_task": UpdateTaskInput,
    "complete_task": CompleteTaskInput,
    "prioritize_task": PrioritizeTaskInput,
    "delete_task": DeleteTaskInput,
    "restore_task": RestoreTaskInput,
    "move_task_to_project": MoveTaskToProjectInput,

    # Projects
    "create_project": CreateProjectInput,
    "update_project": UpdateProjectInput,
    "complete_project": CompleteProjectInput,
    "delete_project": DeleteProjectInput,

    # Books
    "create_book": CreateBookInput,
    "update_book_progress": UpdateBookProgressInput,
    "archive_book": ArchiveBookInput,
    "delete_book": DeleteBookInput,

    # Assets
    "create_asset": CreateAssetInput,
    "update_asset": UpdateAssetInput,
    "delete_asset": DeleteAssetInput,

    # Media
    "upload_media_metadata": UploadMediaMetadataInput,
    "update_media_metadata": UpdateMediaMetadataInput,
    "delete_media_metadata": DeleteMediaMetadataInput,

    # Storage
    "get_storage_status": GetStorageStatusInput,
    "cleanup_storage": CleanupStorageInput,

    # Calendar
    "create_calendar_event": CreateCalendarEventInput,
    "update_calendar_event": UpdateCalendarEventInput,
    "cancel_calendar_event": CancelCalendarEventInput,

    # Habits
    "create_habit": CreateHabitInput,
    "log_habit_checkin": LogHabitCheckinInput,
    "delete_habit": DeleteHabitInput,

    # Quit Addiction
    "create_addiction_tracker": CreateAddictionTrackerInput,
    "log_addiction_relapse": LogAddictionRelapseInput,
    "get_sobriety_stats": GetSobrietyStatsInput,

    # Memory
    "create_memory_item": CreateMemoryItemInput,
    "update_memory_item": UpdateMemoryItemInput,
    "delete_memory_item": DeleteMemoryItemInput,

    # Knowledge
    "create_knowledge_item": CreateKnowledgeItemInput,
    "search_knowledge": SearchKnowledgeInput,
    "delete_knowledge_item": DeleteKnowledgeItemInput,

    # Mission Control
    "get_telemetry_status": GetTelemetryStatusInput,
    "trigger_system_sync": TriggerSystemSyncInput,

    # Settings
    "update_preference": UpdatePreferenceInput,
    "update_reminder_preferences": UpdateReminderPreferencesInput,
    "update_settings_preference": UpdateSettingsPreferenceInput,

    # Trash
    "list_trash_items": ListTrashItemsInput,
    "restore_trash_item": RestoreTrashItemInput,
    "permanent_purge_item": PermanentPurgeItemInput,
    "permanently_delete_item": PermanentlyDeleteItemInput,
    "purge_trash": PurgeTrashInput,

    # New system-level actions
    "get_recent_updates": GetRecentUpdatesInput,
    "get_agent_status": GetAgentStatusInput,
    "reveal_sensitive_config": RevealSensitiveConfigInput,
    "delete_shared_workspace_resources": DeleteSharedWorkspaceResourcesInput,
    "modify_system_policies": ModifySystemPoliciesInput,
    "access_restricted_credentials": AccessRestrictedCredentialsInput,
}
