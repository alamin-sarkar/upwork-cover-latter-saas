import uuid

from pydantic import BaseModel, ConfigDict, Field


class ProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    headline: str | None
    professional_summary: str | None


class ProfileUpdate(BaseModel):
    headline: str | None = Field(default=None, max_length=200)
    professional_summary: str | None = Field(default=None, max_length=2000)


class ProfileSkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    proficiency: str | None = Field(default=None, max_length=40)
    years_experience: int | None = Field(default=None, ge=0, le=60)


class ProfileSkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    proficiency: str | None
    years_experience: int | None
