import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models import (
    Profile,
    ProfileCustomSection,
    ProfileGuideline,
    ProfileProfessionalLife,
    ProfileProject,
    ProfileSample,
    ProfileSkill,
    User,
)
from app.schemas.profile import (
    ProfileCustomSectionCreate,
    ProfileCustomSectionRead,
    ProfileCustomSectionUpdate,
    ProfileGuidelineCreate,
    ProfileGuidelineRead,
    ProfileGuidelineUpdate,
    ProfileProfessionalLifeCreate,
    ProfileProfessionalLifeRead,
    ProfileProfessionalLifeUpdate,
    ProfileProjectCreate,
    ProfileProjectRead,
    ProfileProjectUpdate,
    ProfileRead,
    ProfileSampleCreate,
    ProfileSkillCreate,
    ProfileSkillRead,
    ProfileSampleRead,
    ProfileSampleUpdate,
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


def _parse_uuid_or_404(raw_id: str, detail: str) -> uuid.UUID:
    try:
        return uuid.UUID(raw_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail) from exc

@router.get("", response_model=ProfileRead)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileRead:
    return ProfileRead.model_validate(_get_or_create_profile(db, current_user.id))

@router.put("", response_model=ProfileRead)
def update_profile(payload: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProfileRead:
    profile = _get_or_create_profile(db, current_user.id)
    profile.headline = payload.headline
    profile.professional_summary = payload.professional_summary
    db.commit(); db.refresh(profile)
    return ProfileRead.model_validate(profile)

@router.get("/skills", response_model=list[ProfileSkillRead])
def list_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    return [ProfileSkillRead.model_validate(x) for x in db.scalars(select(ProfileSkill).where(ProfileSkill.profile_id == profile.id).order_by(ProfileSkill.created_at.desc())).all()]

@router.post("/skills", response_model=ProfileSkillRead, status_code=status.HTTP_201_CREATED)
def add_skill(payload: ProfileSkillCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileSkill(profile_id=profile.id, name=payload.name.strip(), proficiency=payload.proficiency, years_experience=payload.years_experience)
    db.add(row)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Skill already exists") from exc
    db.refresh(row)
    return ProfileSkillRead.model_validate(row)

@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileSkill).where(ProfileSkill.id == _parse_uuid_or_404(skill_id, "Skill not found"), ProfileSkill.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(row); db.commit()

@router.get("/projects", response_model=list[ProfileProjectRead])
def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    return [ProfileProjectRead.model_validate(x) for x in db.scalars(select(ProfileProject).where(ProfileProject.profile_id == profile.id).order_by(ProfileProject.created_at.desc())).all()]

@router.post("/projects", response_model=ProfileProjectRead, status_code=status.HTTP_201_CREATED)
def add_project(payload: ProfileProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileProject(profile_id=profile.id, **payload.model_dump())
    row.title = row.title.strip()
    db.add(row); db.commit(); db.refresh(row)
    return ProfileProjectRead.model_validate(row)

@router.patch("/projects/{project_id}", response_model=ProfileProjectRead)
def patch_project(project_id: str, payload: ProfileProjectUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileProject).where(ProfileProject.id == _parse_uuid_or_404(project_id, "Project not found"), ProfileProject.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail="Project not found")
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(row,k,v.strip() if isinstance(v,str) else v)
    db.commit(); db.refresh(row)
    return ProfileProjectRead.model_validate(row)

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileProject).where(ProfileProject.id == _parse_uuid_or_404(project_id, "Project not found"), ProfileProject.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail="Project not found")
    db.delete(row); db.commit()

@router.get('/professional-life', response_model=list[ProfileProfessionalLifeRead])
def list_professional_life(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    return [ProfileProfessionalLifeRead.model_validate(x) for x in db.scalars(select(ProfileProfessionalLife).where(ProfileProfessionalLife.profile_id == profile.id).order_by(ProfileProfessionalLife.created_at.desc())).all()]

@router.post('/professional-life', response_model=ProfileProfessionalLifeRead, status_code=status.HTTP_201_CREATED)
def add_professional_life(payload: ProfileProfessionalLifeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileProfessionalLife(profile_id=profile.id, **payload.model_dump())
    row.company=row.company.strip(); row.role_title=row.role_title.strip()
    db.add(row); db.commit(); db.refresh(row)
    return ProfileProfessionalLifeRead.model_validate(row)

@router.patch('/professional-life/{entry_id}', response_model=ProfileProfessionalLifeRead)
def patch_professional_life(entry_id: str, payload: ProfileProfessionalLifeUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileProfessionalLife).where(ProfileProfessionalLife.id == _parse_uuid_or_404(entry_id, 'Professional life entry not found'), ProfileProfessionalLife.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail='Professional life entry not found')
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(row,k,v.strip() if isinstance(v,str) else v)
    db.commit(); db.refresh(row)
    return ProfileProfessionalLifeRead.model_validate(row)

@router.delete('/professional-life/{entry_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_professional_life(entry_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileProfessionalLife).where(ProfileProfessionalLife.id == _parse_uuid_or_404(entry_id, 'Professional life entry not found'), ProfileProfessionalLife.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail='Professional life entry not found')
    db.delete(row); db.commit()

@router.get('/custom-sections', response_model=list[ProfileCustomSectionRead])
def list_custom_sections(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    return [ProfileCustomSectionRead.model_validate(x) for x in db.scalars(select(ProfileCustomSection).where(ProfileCustomSection.profile_id == profile.id).order_by(ProfileCustomSection.created_at.desc())).all()]

@router.post('/custom-sections', response_model=ProfileCustomSectionRead, status_code=status.HTTP_201_CREATED)
def add_custom_section(payload: ProfileCustomSectionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileCustomSection(profile_id=profile.id, section_name=payload.section_name.strip(), content=payload.content)
    db.add(row); db.commit(); db.refresh(row)
    return ProfileCustomSectionRead.model_validate(row)

@router.patch('/custom-sections/{section_id}', response_model=ProfileCustomSectionRead)
def patch_custom_section(section_id: str, payload: ProfileCustomSectionUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileCustomSection).where(ProfileCustomSection.id == _parse_uuid_or_404(section_id, 'Custom section not found'), ProfileCustomSection.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail='Custom section not found')
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(row,k,v.strip() if isinstance(v,str) else v)
    db.commit(); db.refresh(row)
    return ProfileCustomSectionRead.model_validate(row)

@router.delete('/custom-sections/{section_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_custom_section(section_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileCustomSection).where(ProfileCustomSection.id == _parse_uuid_or_404(section_id, 'Custom section not found'), ProfileCustomSection.profile_id == profile.id))
    if not row: raise HTTPException(status_code=404, detail='Custom section not found')
    db.delete(row); db.commit()

@router.get('/guidelines', response_model=list[ProfileGuidelineRead])
def list_guidelines(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    rows = db.scalars(select(ProfileGuideline).where(ProfileGuideline.profile_id==profile.id).order_by(ProfileGuideline.priority.asc(), ProfileGuideline.created_at.desc())).all()
    return [ProfileGuidelineRead.model_validate(x) for x in rows]

@router.post('/guidelines', response_model=ProfileGuidelineRead, status_code=status.HTTP_201_CREATED)
def add_guideline(payload: ProfileGuidelineCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileGuideline(profile_id=profile.id, title=payload.title.strip(), content=payload.content, priority=payload.priority)
    db.add(row); db.commit(); db.refresh(row)
    return ProfileGuidelineRead.model_validate(row)

@router.patch('/guidelines/{guideline_id}', response_model=ProfileGuidelineRead)
def patch_guideline(guideline_id:str, payload: ProfileGuidelineUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileGuideline).where(ProfileGuideline.id==_parse_uuid_or_404(guideline_id,'Guideline not found'), ProfileGuideline.profile_id==profile.id))
    if not row: raise HTTPException(status_code=404, detail='Guideline not found')
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(row,k,v.strip() if isinstance(v,str) else v)
    db.commit(); db.refresh(row)
    return ProfileGuidelineRead.model_validate(row)

@router.delete('/guidelines/{guideline_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_guideline(guideline_id:str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileGuideline).where(ProfileGuideline.id==_parse_uuid_or_404(guideline_id,'Guideline not found'), ProfileGuideline.profile_id==profile.id))
    if not row: raise HTTPException(status_code=404, detail='Guideline not found')
    db.delete(row); db.commit()

@router.get('/samples', response_model=list[ProfileSampleRead])
def list_samples(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    return [ProfileSampleRead.model_validate(x) for x in db.scalars(select(ProfileSample).where(ProfileSample.profile_id==profile.id).order_by(ProfileSample.created_at.desc())).all()]

@router.post('/samples', response_model=ProfileSampleRead, status_code=status.HTTP_201_CREATED)
def add_sample(payload: ProfileSampleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = ProfileSample(profile_id=profile.id, title=payload.title.strip(), body=payload.body, tone=payload.tone)
    db.add(row); db.commit(); db.refresh(row)
    return ProfileSampleRead.model_validate(row)

@router.patch('/samples/{sample_id}', response_model=ProfileSampleRead)
def patch_sample(sample_id:str, payload: ProfileSampleUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileSample).where(ProfileSample.id==_parse_uuid_or_404(sample_id,'Sample not found'), ProfileSample.profile_id==profile.id))
    if not row: raise HTTPException(status_code=404, detail='Sample not found')
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(row,k,v.strip() if isinstance(v,str) else v)
    db.commit(); db.refresh(row)
    return ProfileSampleRead.model_validate(row)

@router.delete('/samples/{sample_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(sample_id:str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, current_user.id)
    row = db.scalar(select(ProfileSample).where(ProfileSample.id==_parse_uuid_or_404(sample_id,'Sample not found'), ProfileSample.profile_id==profile.id))
    if not row: raise HTTPException(status_code=404, detail='Sample not found')
    db.delete(row); db.commit()
