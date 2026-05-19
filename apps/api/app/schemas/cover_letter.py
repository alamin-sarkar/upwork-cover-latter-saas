import uuid

from pydantic import BaseModel, ConfigDict, Field


class JobPostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    raw_text: str = Field(min_length=30, max_length=30000)
    source: str = Field(default="upwork", max_length=40)


class JobPostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    raw_text: str
    source: str


class GenerateCoverLetterRequest(BaseModel):
    job_post_id: uuid.UUID


class CoverLetterVariantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    structure: str
    analysis_summary: str
    draft_text: str


class CoverLetterFeedbackCreate(BaseModel):
    generation_id: uuid.UUID
    rating: int = Field(ge=1, le=5)
    feedback_text: str | None = Field(default=None, max_length=3000)


class CoverLetterFeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    generation_id: uuid.UUID
    rating: int
    feedback_text: str | None


class CoverLetterMemorySignalRead(BaseModel):
    avg_rating: float | None
    preferred_tone: str | None
    do_more: list[str]
    avoid: list[str]
