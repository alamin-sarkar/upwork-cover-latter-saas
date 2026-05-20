import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ClientResponseOutcome(StrEnum):
    no_response = "no_response"
    replied = "replied"
    interview = "interview"
    hired = "hired"
    rejected = "rejected"


class CoverLetterFeedbackBase(BaseModel):
    rating: int = Field(ge=1, le=5)
    edited_cover_letter: str | None = Field(default=None, min_length=1)
    accepted_sections: list[str] = Field(default_factory=list, max_length=20)
    rejected_sections: list[str] = Field(default_factory=list, max_length=20)
    client_response_outcome: ClientResponseOutcome = ClientResponseOutcome.no_response
    notes: str | None = Field(default=None, max_length=4000)


class CoverLetterFeedbackCreate(CoverLetterFeedbackBase):
    generation_variant_id: uuid.UUID


class CoverLetterFeedbackUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    edited_cover_letter: str | None = Field(default=None, min_length=1)
    accepted_sections: list[str] | None = Field(default=None, max_length=20)
    rejected_sections: list[str] | None = Field(default=None, max_length=20)
    client_response_outcome: ClientResponseOutcome | None = None
    notes: str | None = Field(default=None, max_length=4000)


class CoverLetterFeedbackOut(CoverLetterFeedbackBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    generation_run_id: uuid.UUID
    generation_variant_id: uuid.UUID
    memory_text: str
    created_at: datetime
    updated_at: datetime
