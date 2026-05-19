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


class ProfileSkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
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


class ProfileProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
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


class ProfileProfessionalLifeUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role_title: str | None = Field(default=None, min_length=1, max_length=200)
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


class ProfileCustomSectionUpdate(BaseModel):
    section_name: str | None = Field(default=None, min_length=1, max_length=120)
    content: str | None = Field(default=None, min_length=1, max_length=5000)


class ProfileCustomSectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    section_name: str
    content: str


class ProfileGuidelineCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1, max_length=5000)
    priority: int = Field(default=100, ge=1, le=1000)


class ProfileGuidelineUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    priority: int | None = Field(default=None, ge=1, le=1000)


class ProfileGuidelineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    priority: int


class ProfileSampleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=7000)
    tone: str | None = Field(default=None, max_length=80)


class ProfileSampleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = Field(default=None, min_length=1, max_length=7000)
    tone: str | None = Field(default=None, max_length=80)


class ProfileSampleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    body: str
    tone: str | None
