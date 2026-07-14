from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CopilotPlannerOutput(BaseModel):
    message_to_user: Optional[str] = Field(default=None, description="Direct text response to display to the user.")
    action_name: Optional[str] = Field(default=None, description="The name of the action to execute, if any.")
    action_payload: Optional[Dict[str, Any]] = Field(default=None, description="Parameters mapping to the Pydantic schema of the action.")
    requires_clarification: bool = Field(default=False, description="Set to true if user needs to clarify parameters or intent.")
    clarification_question: Optional[str] = Field(default=None, description="Question text to ask the user for clarification.")
    confidence: float = Field(default=1.0, description="Confidence score from 0.0 to 1.0.")
    refusal_reason: Optional[str] = Field(default=None, description="Reason for refusing execution.")
