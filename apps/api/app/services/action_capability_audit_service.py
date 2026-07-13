from typing import List, Dict, Any
from app.services.action_registry import ActionRegistry

class ActionCapabilityAuditService:
    @classmethod
    def audit_capabilities(cls) -> Dict[str, Any]:
        """
        Audits the registered actions and classifies them.
        """
        registered = ActionRegistry.list_actions()
        
        # Action classifications
        working = ["create_lesson_note", "save_corrected_example", "update_preference", "mark_pattern_mastered"]
        blocked = ["delete_all_files"]
        missing = ["create_project_item", "update_project_item", "create_calendar_event", "create_memory_item"]
        
        report = {
            "total_registered": len(registered),
            "working_actions": [],
            "blocked_actions": [],
            "missing_actions": [],
            "unsupported_actions": []
        }
        
        for name in registered:
            if name in working:
                report["working_actions"].append(name)
            elif name in blocked:
                report["blocked_actions"].append(name)
            elif name in missing:
                report["missing_actions"].append(name)
            else:
                report["unsupported_actions"].append(name)
                
        return report
