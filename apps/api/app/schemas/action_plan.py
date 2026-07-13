from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ActionPlanStep(BaseModel):
    action_name: str
    payload: Dict[str, Any]

class ActionPlan(BaseModel):
    goal: str = Field(..., description="The ultimate target state or goal of the workflow.")
    reasoning_summary: str = Field(..., description="Justification explaining why these steps achieve the goal.")
    steps: List[ActionPlanStep] = Field(default_factory=list, description="Ordered execution items.")
    requires_approval: bool = Field(default=True, description="Indicates if plan has high-risk steps.")
    estimated_risk: float = Field(default=1.0, description="Risk assessment score between 0.0 and 1.0.")
    stop_conditions: List[str] = Field(default_factory=list, description="Explicit failure thresholds.")
    fallback_behavior: str = Field(default="rollback", description="Rollback policy on intermediate failures.")
