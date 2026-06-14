from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class DiagnoseTextRequest(BaseModel):
    text: str
    lang: str = "fr"
    mode: str = "beginner"
    context: Optional[dict] = None

class CauseItem(BaseModel):
    description: str
    probability: float

class StepItem(BaseModel):
    step: int
    instruction: str
    command: Optional[str] = None

class CommandItem(BaseModel):
    os: str
    command: str
    desc: str

class DiagnosticResponse(BaseModel):
    id: UUID
    code: Optional[str]
    title: str
    category: str
    detected_system: str
    confidence: float
    severity: str
    causes: List[CauseItem]
    impact: Optional[str]
    procedure_quick: List[StepItem]
    procedure_advanced: Optional[List[StepItem]]
    commands: Optional[List[CommandItem]]
    prevention: Optional[str]
    is_offline: bool = False
    created_at: datetime

    class Config:
        from_attributes = True