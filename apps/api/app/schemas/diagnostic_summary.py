from pydantic import BaseModel
from typing import Dict

class DiagnosticSummary(BaseModel):
    total_reports: int
    severity_counts: Dict[str, int]
    type_counts: Dict[str, int]
