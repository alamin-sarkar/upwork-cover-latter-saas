import uuid
from datetime import datetime

from ai_workflows.generation.schemas import CoverLetterStructure
from ai_workflows.job_analysis.schemas import JobAnalysis
from pydantic import BaseModel, Field, model_validator


class CoverLetterGenerateRequest(BaseModel):
    raw_job_text: str | None = Field(default=None, min_length=20, max_length=50000)
    analysis_snapshot_id: uuid.UUID | None = None
    structures: list[CoverLetterStructure] | None = None

    @model_validator(mode="after")
    def validate_source(self):
        if not self.raw_job_text and not self.analysis_snapshot_id:
            raise ValueError("Either raw_job_text or analysis_snapshot_id must be provided")
        return self


class CoverLetterVariantOut(BaseModel):
    id: uuid.UUID
    structure: CoverLetterStructure
    headline: str
    cover_letter: str
    rationale: str
    match_notes: list[str]
    self_check_notes: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class CoverLetterGenerationResponse(BaseModel):
    id: uuid.UUID
    analysis_snapshot_id: uuid.UUID
    raw_job_text: str
    prompt_version: str
    requested_structures: list[CoverLetterStructure]
    analysis: JobAnalysis
    variants: list[CoverLetterVariantOut]
    created_at: datetime

    model_config = {"from_attributes": True}
