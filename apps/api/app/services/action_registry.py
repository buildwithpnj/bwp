from typing import Dict, Any, List, Optional

class ActionRegistry:
    # Centrally defined dictionary of safe tools metadata and schemas
    ACTIONS = {
        "save_corrected_example": {
            "description": "Saves a corrected sentence and its explanation to the user library.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "original": str,
                "corrected": str,
                "explanation": str
            }
        },
        "create_lesson_note": {
            "description": "Saves a learning or lesson note card from the conversation.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "title": str,
                "content": str
            }
        },
        "create_note": {
            "description": "Creates a new workspace note.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "title": str,
                "content": str
            }
        },
        "update_note": {
            "description": "Updates an existing note's title and content.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "note_id": str,
                "title": str,
                "content": str
            }
        },
        "create_task": {
            "description": "Creates a new operational task.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "title": str
            }
        },
        "update_task": {
            "description": "Updates task status and progress.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "task_id": str,
                "status": str
            }
        },
        "complete_task": {
            "description": "Marks a task as completed.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "task_id": str
            }
        },
        "create_project_item": {
            "description": "Creates a new project item tracking entry.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "name": str
            }
        },
        "update_project_item": {
            "description": "Updates a project item's status.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "project_id": str,
                "status": str
            }
        },
        "create_calendar_event": {
            "description": "Creates a new calendar event entry.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "title": str,
                "start_time": str,
                "end_time": str
            }
        },
        "create_memory_item": {
            "description": "Adds a fact or trait to user memory.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "fact": str
            }
        },
        "search_knowledge": {
            "description": "Searches the workspace knowledge base.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "query": str
            }
        },
        "get_recent_updates": {
            "description": "Retrieves recent changes across modules.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "limit": int
            }
        },
        "update_preference": {
            "description": "Updates tone, explanation style, target level, or language support preferences.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "tone": str,
                "explanation_style": str
            }
        },
        "mark_pattern_mastered": {
            "description": "Marks a specific grammar or correction pattern as mastered.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "pattern_name": str
            }
        },
        "create_followup_practice": {
            "description": "Generates and logs a practice task reminder for later.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": True,  # Higher-risk reminder tasks require user approval
            "input_schema": {
                "task_description": str
            }
        },
        "create_summary_note": {
            "description": "Generates a summary of the current user conversation context.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "topic": str,
                "notes": str
            }
        },
        "generate_weekly_review": {
            "description": "Aggregates learning metrics for the week.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "week_offset": int
            }
        },
        "build_practice_plan": {
            "description": "Assembles a custom checklist of correction practices.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": True,
            "input_schema": {
                "focus_area": str,
                "num_tasks": int
            }
        },
        "schedule_followup_check": {
            "description": "Sets a timed callback for feedback reviews.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": True,
            "input_schema": {
                "due_hours": int
            }
        },
        "update_reminder_preferences": {
            "description": "Customizes frequency of notifications.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "frequency": str
            }
        },
        "generate_contextual_coaching_prompt": {
            "description": "Drafts a custom coaching prompt based on weakness areas.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": False,
            "input_schema": {
                "weakness": str
            }
        },
        "create_parent_checkin_summary": {
            "description": "Creates a study progress email report draft.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": True,
            "input_schema": {
                "parent_email": str,
                "progress_percentage": int
            }
        },
        "prepare_escalation_message_draft": {
            "description": "Drafts an escalation message when confidence score drops.",
            "allowed_roles": ["approved_user", "internal_admin"],
            "requires_approval": True,
            "input_schema": {
                "reason": str
            }
        },
        "delete_all_files": {
            "description": "Deletes all files in the system.",
            "allowed_roles": ["internal_admin"],
            "requires_approval": True,
            "input_schema": {}
        }
    }

    @classmethod
    def get_action(cls, action_name: str) -> Optional[Dict[str, Any]]:
        return cls.ACTIONS.get(action_name)

    @classmethod
    def list_actions(cls) -> List[str]:
        return list(cls.ACTIONS.keys())

    @classmethod
    def validate_inputs(cls, action_name: str, payload: Dict[str, Any]) -> bool:
        action = cls.get_action(action_name)
        if not action:
            return False
            
        schema = action["input_schema"]
        for key, expected_type in schema.items():
            if key not in payload:
                return False
            if not isinstance(payload[key], expected_type):
                return False
        return True
