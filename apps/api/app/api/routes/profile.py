import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models import Profile, ProfileCustomSection, ProfileProfessionalLife, ProfileProject, ProfileSkill, User
from app.schemas import (
    ProfileCustomSectionCreate,
    ProfileCustomSectionRead,
    ProfileProfessionalLifeCreate,
    ProfileProfessionalLifeRead,
    ProfileProjectCreate,
    ProfileProjectRead,
    ProfileRead,
    ProfileSkillCreate,
    ProfileSkillRead,
    ProfileUpdate,
)

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


def _get_or_create_profile(db: Session, user_id) -> Profile:
    profile = db.scalar(select(Profile).where(Profile.user_id == user_id))
    if profile:
        return profile

    profile = Profile(user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=ProfileRead)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileRead:
    profile = _get_or_create_profile(db, current_user.id)
    return ProfileRead.model_validate(profile)


@router.put("", response_model=ProfileRead)
def update_profile(payload: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileRead:
    profile = _get_or_create_profile(db, current_user.id)
    profile.headline = payload.headline
    profile.professional_summary = payload.professional_summary
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return ProfileRead.model_validate(profile)


@router.get("/skills", response_model=list[ProfileSkillRead])
def list_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProfileSkillRead]:
    profile = _get_or_create_profile(db, current_user.id)
    skills = db.scalars(select(ProfileSkill).where(ProfileSkill.profile_id == profile.id).order_by(ProfileSkill.created_at.desc())).all()
    return [ProfileSkillRead.model_validate(skill) for skill in skills]


@router.post("/skills", response_model=ProfileSkillRead, status_code=status.HTTP_201_CREATED)
def add_skill(payload: ProfileSkillCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileSkillRead:
    profile = _get_or_create_profile(db, current_user.id)
    skill = ProfileSkill(
        profile_id=profile.id,
        name=payload.name.strip(),
        proficiency=payload.proficiency,
        years_experience=payload.years_experience,
    )
    db.add(skill)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Skill already exists") from exc
    db.refresh(skill)
    return ProfileSkillRead.model_validate(skill)


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    profile = _get_or_create_profile(db, current_user.id)
    try:
        skill_uuid = uuid.UUID(skill_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found") from exc
    skill = db.scalar(select(ProfileSkill).where(ProfileSkill.id == skill_uuid, ProfileSkill.profile_id == profile.id))
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    db.delete(skill)
    db.commit()


@router.get("/projects", response_model=list[ProfileProjectRead])
def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProfileProjectRead]:
    profile = _get_or_create_profile(db, current_user.id)
    projects = db.scalars(select(ProfileProject).where(ProfileProject.profile_id == profile.id).order_by(ProfileProject.created_at.desc())).all()
    return [ProfileProjectRead.model_validate(project) for project in projects]


@router.post("/projects", response_model=ProfileProjectRead, status_code=status.HTTP_201_CREATED)
def add_project(payload: ProfileProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileProjectRead:
    profile = _get_or_create_profile(db, current_user.id)
    project = ProfileProject(
        profile_id=profile.id,
        title=payload.title.strip(),
        description=payload.description,
        tech_stack=payload.tech_stack,
        impact=payload.impact,
        project_url=payload.project_url,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProfileProjectRead.model_validate(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    profile = _get_or_create_profile(db, current_user.id)
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found") from exc
    project = db.scalar(select(ProfileProject).where(ProfileProject.id == project_uuid, ProfileProject.profile_id == profile.id))
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()


@router.get("/professional-life", response_model=list[ProfileProfessionalLifeRead])
def list_professional_life(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProfileProfessionalLifeRead]:
    profile = _get_or_create_profile(db, current_user.id)
    rows = db.scalars(select(ProfileProfessionalLife).where(ProfileProfessionalLife.profile_id == profile.id).order_by(ProfileProfessionalLife.created_at.desc())).all()
    return [ProfileProfessionalLifeRead.model_validate(row) for row in rows]


@router.post("/professional-life", response_model=ProfileProfessionalLifeRead, status_code=status.HTTP_201_CREATED)
def add_professional_life(payload: ProfileProfessionalLifeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileProfessionalLifeRead:
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileProfessionalLife(
        profile_id=profile.id,
        company=payload.company.strip(),
        role_title=payload.role_title.strip(),
        start_date=payload.start_date,
        end_date=payload.end_date,
        summary=payload.summary,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ProfileProfessionalLifeRead.model_validate(row)


@router.delete("/professional-life/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professional_life(entry_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    profile = _get_or_create_profile(db, current_user.id)
    try:
        entry_uuid = uuid.UUID(entry_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional life entry not found") from exc
    row = db.scalar(select(ProfileProfessionalLife).where(ProfileProfessionalLife.id == entry_uuid, ProfileProfessionalLife.profile_id == profile.id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional life entry not found")
    db.delete(row)
    db.commit()


@router.get("/custom-sections", response_model=list[ProfileCustomSectionRead])
def list_custom_sections(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProfileCustomSectionRead]:
    profile = _get_or_create_profile(db, current_user.id)
    rows = db.scalars(select(ProfileCustomSection).where(ProfileCustomSection.profile_id == profile.id).order_by(ProfileCustomSection.created_at.desc())).all()
    return [ProfileCustomSectionRead.model_validate(row) for row in rows]


@router.post("/custom-sections", response_model=ProfileCustomSectionRead, status_code=status.HTTP_201_CREATED)
def add_custom_section(payload: ProfileCustomSectionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileCustomSectionRead:
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileCustomSection(profile_id=profile.id, section_name=payload.section_name.strip(), content=payload.content)
    db.add(row)
    db.commit()
    db.refresh(row)
    return ProfileCustomSectionRead.model_validate(row)


@router.delete("/custom-sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_custom_section(section_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    profile = _get_or_create_profile(db, current_user.id)
    try:
        section_uuid = uuid.UUID(section_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Custom section not found") from exc
    row = db.scalar(select(ProfileCustomSection).where(ProfileCustomSection.id == section_uuid, ProfileCustomSection.profile_id == profile.id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Custom section not found")
    db.delete(row)
    db.commit()
