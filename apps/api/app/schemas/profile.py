import uuid
from datetime import date

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


class ProfileProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=3000)
    tech_stack: str | None = Field(default=None, max_length=500)
    impact: str | None = Field(default=None, max_length=500)
    project_url: str | None = Field(default=None, max_length=500)


class ProfileProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    tech_stack: str | None
    impact: str | None
    project_url: str | None


class ProfileProfessionalLifeCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role_title: str = Field(min_length=1, max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    summary: str | None = Field(default=None, max_length=3000)


class ProfileProfessionalLifeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company: str
    role_title: str
    start_date: date | None
    end_date: date | None
    summary: str | None


class ProfileCustomSectionCreate(BaseModel):
    section_name: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=5000)


class ProfileCustomSectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    section_name: str
    content: str
