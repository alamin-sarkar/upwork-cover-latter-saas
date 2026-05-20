import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileBase(BaseModel):
    professional_title: str | None = Field(default=None, max_length=200)
    location: str | None = Field(default=None, max_length=200)
    hourly_rate_usd: float | None = Field(default=None, ge=0, le=10000)
    about: str | None = None
    availability_note: str | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    professional_title: str | None = Field(default=None, max_length=200)
    location: str | None = Field(default=None, max_length=200)
    hourly_rate_usd: float | None = Field(default=None, ge=0, le=10000)
    about: str | None = None
    availability_note: str | None = None


class ProfileSkillBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    level: str | None = Field(default=None, max_length=50)
    years_of_experience: float | None = Field(default=None, ge=0, le=60)
    proof: str | None = None
    sort_order: int = Field(default=0, ge=0, le=10000)


class ProfileSkillCreate(ProfileSkillBase):
    pass


class ProfileSkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    level: str | None = Field(default=None, max_length=50)
    years_of_experience: float | None = Field(default=None, ge=0, le=60)
    proof: str | None = None
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class ProfileProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    role: str | None = Field(default=None, max_length=120)
    tagline: str | None = Field(default=None, max_length=240)
    description: str = Field(min_length=1)
    outcome: str | None = None
    link: str | None = Field(default=None, max_length=500)
    stack: list[str] = Field(default_factory=list)
    evidence_points: list[str] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0, le=10000)


class ProfileProjectCreate(ProfileProjectBase):
    pass


class ProfileProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, max_length=120)
    tagline: str | None = Field(default=None, max_length=240)
    description: str | None = Field(default=None, min_length=1)
    outcome: str | None = None
    link: str | None = Field(default=None, max_length=500)
    stack: list[str] | None = None
    evidence_points: list[str] | None = None
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class ProfileExperienceBase(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    summary: str | None = None
    highlights: list[str] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0, le=10000)

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, value: date | None, info) -> date | None:
        start_date = info.data.get("start_date")
        if value and start_date and value < start_date:
            raise ValueError("end_date must be on or after start_date")
        return value


class ProfileExperienceCreate(ProfileExperienceBase):
    pass


class ProfileExperienceUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, min_length=1, max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None
    summary: str | None = None
    highlights: list[str] | None = None
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class ProfileNicheBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    summary: str | None = None
    proof: str | None = None
    sort_order: int = Field(default=0, ge=0, le=10000)


class ProfileNicheCreate(ProfileNicheBase):
    pass


class ProfileNicheUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    summary: str | None = None
    proof: str | None = None
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class ProfileCustomSectionBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    section_type: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1)
    sort_order: int = Field(default=0, ge=0, le=10000)


class ProfileCustomSectionCreate(ProfileCustomSectionBase):
    pass


class ProfileCustomSectionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    section_type: str | None = Field(default=None, min_length=1, max_length=80)
    content: str | None = Field(default=None, min_length=1)
    sort_order: int | None = Field(default=None, ge=0, le=10000)


class ProfilePreferencesBase(BaseModel):
    default_tone: str | None = Field(default=None, max_length=80)
    voice_note: str | None = None
    avoid_phrases: list[str] = Field(default_factory=list)
    preferred_length: str | None = Field(default=None, max_length=40)
    cta_style: str | None = Field(default=None, max_length=80)
    signature: str | None = None
    extra_instructions: str | None = None


class ProfilePreferencesCreate(ProfilePreferencesBase):
    pass


class ProfilePreferencesUpdate(BaseModel):
    default_tone: str | None = Field(default=None, max_length=80)
    voice_note: str | None = None
    avoid_phrases: list[str] | None = None
    preferred_length: str | None = Field(default=None, max_length=40)
    cta_style: str | None = Field(default=None, max_length=80)
    signature: str | None = None
    extra_instructions: str | None = None


class ProfileOut(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileSkillOut(ProfileSkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileProjectOut(ProfileProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileExperienceOut(ProfileExperienceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileNicheOut(ProfileNicheBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileCustomSectionOut(ProfileCustomSectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfilePreferencesOut(ProfilePreferencesBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProfileDetailOut(ProfileOut):
    skills: list[ProfileSkillOut] = Field(default_factory=list)
    projects: list[ProfileProjectOut] = Field(default_factory=list)
    experiences: list[ProfileExperienceOut] = Field(default_factory=list)
    niches: list[ProfileNicheOut] = Field(default_factory=list)
    custom_sections: list[ProfileCustomSectionOut] = Field(default_factory=list)
    preferences: ProfilePreferencesOut | None = None
