from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models import Profile, ProfileSkill, User
from app.schemas import ProfileRead, ProfileSkillCreate, ProfileSkillRead, ProfileUpdate

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
    skill = db.scalar(select(ProfileSkill).where(ProfileSkill.id == skill_id, ProfileSkill.profile_id == profile.id))
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    db.delete(skill)
    db.commit()
