from enum import StrEnum

from pydantic import BaseModel, Field


class JobUrgency(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class JobTone(StrEnum):
    formal = "formal"
    neutral = "neutral"
    friendly = "friendly"
    demanding = "demanding"


class JobAnalysis(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    scope: str = Field(min_length=1)
    deliverables: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    budget_clues: list[str] = Field(default_factory=list)
    urgency: JobUrgency
    tone: JobTone
    risk_flags: list[str] = Field(default_factory=list)
    fit_score: int = Field(ge=0, le=100)
