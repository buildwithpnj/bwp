import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("action_persistence_guard")

class ActionPersistenceGuard:
    @classmethod
    def validate_write_safety(cls, action_name: str, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Applies write safety checks to incoming actions before they touch the database.
        """
        # Note write protections
        if action_name in ("create_note", "create_lesson_note", "update_note"):
            title = payload.get("title", "")
            if len(title) > 255:
                return False, "Title length exceeds 255 character limit."
            if not title.strip():
                return False, "Title must contain non-whitespace characters."
                
        # Task write protections
        if action_name == "create_task":
            title = payload.get("title", "")
            if len(title) > 255:
                return False, "Task title exceeds 255 character limit."
            if not title.strip():
                return False, "Task title cannot be empty."
                
        # Project item protections
        if action_name == "create_project_item":
            name = payload.get("name", "")
            if len(name) > 255:
                return False, "Project item name exceeds 255 character limit."
            if not name.strip():
                return False, "Project item name cannot be empty."
                
        if action_name == "delete_all_files":
            return False, "Safety validation blocked: dangerous operation."
            
        return True, "Safety validations passed."
