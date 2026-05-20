import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class GuidelineType(StrEnum):
    rule = "rule"
    intro = "intro"
    cta = "cta"
    tone_preset = "tone_preset"


class SampleTag(StrEnum):
    winning = "winning"
    anti_pattern = "anti-pattern"


class CoverLetterGuidelineBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    guideline_type: GuidelineType
    description: str | None = None
    content: str = Field(min_length=1)
    sort_order: int = Field(default=0, ge=0, le=10000)


class CoverLetterGuidelineCreate(CoverLetterGuidelineBase):
    pass


class CoverLetterGuidelineUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    guideline_type: GuidelineType | None = None
    description: str | None = None
    content: str | None = Field(default=None, min_length=1)
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class CoverLetterGuidelineOut(CoverLetterGuidelineBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CoverLetterSampleBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    tag: SampleTag
    content: str = Field(min_length=1)
    notes: str | None = None
    outcome: str | None = None
    sort_order: int = Field(default=0, ge=0, le=10000)


class CoverLetterSampleCreate(CoverLetterSampleBase):
    pass


class CoverLetterSampleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    tag: SampleTag | None = None
    content: str | None = Field(default=None, min_length=1)
    notes: str | None = None
    outcome: str | None = None
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class CoverLetterSampleOut(CoverLetterSampleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
