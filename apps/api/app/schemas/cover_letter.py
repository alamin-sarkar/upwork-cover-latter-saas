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
