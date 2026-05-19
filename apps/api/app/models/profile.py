import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    headline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    professional_summary: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    skills: Mapped[list["ProfileSkill"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
    projects: Mapped[list["ProfileProject"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
    professional_life_entries: Mapped[list["ProfileProfessionalLife"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
    custom_sections: Mapped[list["ProfileCustomSection"]] = relationship(back_populates="profile", cascade="all, delete-orphan")


class ProfileSkill(Base):
    __tablename__ = "profile_skills"
    __table_args__ = (UniqueConstraint("profile_id", "name", name="uq_profile_skill_name"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    proficiency: Mapped[str | None] = mapped_column(String(40), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    profile: Mapped[Profile] = relationship(back_populates="skills")


class ProfileProject(Base):
    __tablename__ = "profile_projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(3000), nullable=True)
    tech_stack: Mapped[str | None] = mapped_column(String(500), nullable=True)
    impact: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    profile: Mapped[Profile] = relationship(back_populates="projects")


class ProfileProfessionalLife(Base):
    __tablename__ = "profile_professional_life"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    role_title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    summary: Mapped[str | None] = mapped_column(String(3000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    profile: Mapped[Profile] = relationship(back_populates="professional_life_entries")


class ProfileCustomSection(Base):
    __tablename__ = "profile_custom_sections"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    section_name: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    profile: Mapped[Profile] = relationship(back_populates="custom_sections")
