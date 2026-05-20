import uuid
from typing import Any, TypeVar

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.deps import CurrentUser, DbSession
from app.models.profile import (
    Profile,
    ProfileCustomSection,
    ProfileExperience,
    ProfileNiche,
    ProfilePreferences,
    ProfileProject,
    ProfileSkill,
)
from app.models.user import User
from app.schemas.profile import (
    ProfileCreate,
    ProfileCustomSectionCreate,
    ProfileCustomSectionOut,
    ProfileCustomSectionUpdate,
    ProfileDetailOut,
    ProfileExperienceCreate,
    ProfileExperienceOut,
    ProfileExperienceUpdate,
    ProfileNicheCreate,
    ProfileNicheOut,
    ProfileNicheUpdate,
    ProfileOut,
    ProfilePreferencesCreate,
    ProfilePreferencesOut,
    ProfilePreferencesUpdate,
    ProfileProjectCreate,
    ProfileProjectOut,
    ProfileProjectUpdate,
    ProfileSkillCreate,
    ProfileSkillOut,
    ProfileSkillUpdate,
    ProfileUpdate,
)

router = APIRouter(prefix="/profile", tags=["profile"])

SectionModel = TypeVar(
    "SectionModel",
    ProfileSkill,
    ProfileProject,
    ProfileExperience,
    ProfileNiche,
    ProfileCustomSection,
)


def _apply_updates(instance: Any, updates: dict[str, Any]) -> Any:
    for field, value in updates.items():
        setattr(instance, field, value)
    return instance


async def _get_profile(
    session: DbSession,
    user_id: uuid.UUID,
    *,
    eager: bool = False,
) -> Profile | None:
    stmt = select(Profile).where(Profile.user_id == user_id)
    if eager:
        stmt = stmt.options(
            selectinload(Profile.skills),
            selectinload(Profile.projects),
            selectinload(Profile.experiences),
            selectinload(Profile.niches),
            selectinload(Profile.custom_sections),
            selectinload(Profile.preferences),
        )
    return await session.scalar(stmt)


async def _get_profile_or_404(
    session: DbSession,
    user_id: uuid.UUID,
    *,
    eager: bool = False,
) -> Profile:
    profile = await _get_profile(session, user_id, eager=eager)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


async def _get_or_create_profile(session: DbSession, user: User) -> Profile:
    profile = await _get_profile(session, user.id)
    if profile is not None:
        return profile

    profile = Profile(user_id=user.id)
    session.add(profile)
    await session.flush()
    return profile


async def _get_section_item_or_404(
    session: DbSession,
    model: type[SectionModel],
    item_id: uuid.UUID,
    user_id: uuid.UUID,
) -> SectionModel:
    stmt = (
        select(model)
        .join(Profile, model.profile_id == Profile.id)
        .where(model.id == item_id, Profile.user_id == user_id)
    )
    item = await session.scalar(stmt)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return item


async def _list_section_items(
    session: DbSession,
    model: type[SectionModel],
    user_id: uuid.UUID,
) -> list[SectionModel]:
    stmt = (
        select(model)
        .join(Profile, model.profile_id == Profile.id)
        .where(Profile.user_id == user_id)
        .order_by(model.sort_order.asc(), model.created_at.asc())
    )
    return list(await session.scalars(stmt))


@router.post("", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile(
    body: ProfileCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> Profile:
    existing = await _get_profile(session, current_user.id)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    profile = Profile(user_id=current_user.id, **body.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.get("", response_model=ProfileDetailOut)
async def get_profile(current_user: CurrentUser, session: DbSession) -> Profile:
    return await _get_profile_or_404(session, current_user.id, eager=True)


@router.patch("", response_model=ProfileOut)
async def update_profile(
    body: ProfileUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> Profile:
    profile = await _get_profile_or_404(session, current_user.id)
    _apply_updates(profile, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(profile)
    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(current_user: CurrentUser, session: DbSession) -> Response:
    profile = await _get_profile_or_404(session, current_user.id)
    await session.delete(profile)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/skills", response_model=list[ProfileSkillOut])
async def list_skills(current_user: CurrentUser, session: DbSession) -> list[ProfileSkill]:
    return await _list_section_items(session, ProfileSkill, current_user.id)


@router.post("/skills", response_model=ProfileSkillOut, status_code=status.HTTP_201_CREATED)
async def create_skill(
    body: ProfileSkillCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileSkill:
    profile = await _get_or_create_profile(session, current_user)
    skill = ProfileSkill(profile_id=profile.id, **body.model_dump())
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill


@router.get("/skills/{skill_id}", response_model=ProfileSkillOut)
async def get_skill(
    skill_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileSkill:
    return await _get_section_item_or_404(session, ProfileSkill, skill_id, current_user.id)


@router.patch("/skills/{skill_id}", response_model=ProfileSkillOut)
async def update_skill(
    skill_id: uuid.UUID,
    body: ProfileSkillUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileSkill:
    skill = await _get_section_item_or_404(session, ProfileSkill, skill_id, current_user.id)
    _apply_updates(skill, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(skill)
    return skill


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    skill = await _get_section_item_or_404(session, ProfileSkill, skill_id, current_user.id)
    await session.delete(skill)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/projects", response_model=list[ProfileProjectOut])
async def list_projects(current_user: CurrentUser, session: DbSession) -> list[ProfileProject]:
    return await _list_section_items(session, ProfileProject, current_user.id)


@router.post("/projects", response_model=ProfileProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProfileProjectCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileProject:
    profile = await _get_or_create_profile(session, current_user)
    project = ProfileProject(profile_id=profile.id, **body.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProfileProjectOut)
async def get_project(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileProject:
    return await _get_section_item_or_404(session, ProfileProject, project_id, current_user.id)


@router.patch("/projects/{project_id}", response_model=ProfileProjectOut)
async def update_project(
    project_id: uuid.UUID,
    body: ProfileProjectUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileProject:
    project = await _get_section_item_or_404(session, ProfileProject, project_id, current_user.id)
    _apply_updates(project, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    project = await _get_section_item_or_404(session, ProfileProject, project_id, current_user.id)
    await session.delete(project)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/experiences", response_model=list[ProfileExperienceOut])
async def list_experiences(
    current_user: CurrentUser,
    session: DbSession,
) -> list[ProfileExperience]:
    return await _list_section_items(session, ProfileExperience, current_user.id)


@router.post(
    "/experiences",
    response_model=ProfileExperienceOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_experience(
    body: ProfileExperienceCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileExperience:
    profile = await _get_or_create_profile(session, current_user)
    experience = ProfileExperience(profile_id=profile.id, **body.model_dump())
    session.add(experience)
    await session.commit()
    await session.refresh(experience)
    return experience


@router.get("/experiences/{experience_id}", response_model=ProfileExperienceOut)
async def get_experience(
    experience_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileExperience:
    return await _get_section_item_or_404(
        session, ProfileExperience, experience_id, current_user.id
    )


@router.patch("/experiences/{experience_id}", response_model=ProfileExperienceOut)
async def update_experience(
    experience_id: uuid.UUID,
    body: ProfileExperienceUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileExperience:
    experience = await _get_section_item_or_404(
        session, ProfileExperience, experience_id, current_user.id
    )
    _apply_updates(experience, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(experience)
    return experience


@router.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    experience = await _get_section_item_or_404(
        session, ProfileExperience, experience_id, current_user.id
    )
    await session.delete(experience)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/niches", response_model=list[ProfileNicheOut])
async def list_niches(current_user: CurrentUser, session: DbSession) -> list[ProfileNiche]:
    return await _list_section_items(session, ProfileNiche, current_user.id)


@router.post("/niches", response_model=ProfileNicheOut, status_code=status.HTTP_201_CREATED)
async def create_niche(
    body: ProfileNicheCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileNiche:
    profile = await _get_or_create_profile(session, current_user)
    niche = ProfileNiche(profile_id=profile.id, **body.model_dump())
    session.add(niche)
    await session.commit()
    await session.refresh(niche)
    return niche


@router.get("/niches/{niche_id}", response_model=ProfileNicheOut)
async def get_niche(
    niche_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileNiche:
    return await _get_section_item_or_404(session, ProfileNiche, niche_id, current_user.id)


@router.patch("/niches/{niche_id}", response_model=ProfileNicheOut)
async def update_niche(
    niche_id: uuid.UUID,
    body: ProfileNicheUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileNiche:
    niche = await _get_section_item_or_404(session, ProfileNiche, niche_id, current_user.id)
    _apply_updates(niche, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(niche)
    return niche


@router.delete("/niches/{niche_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_niche(
    niche_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    niche = await _get_section_item_or_404(session, ProfileNiche, niche_id, current_user.id)
    await session.delete(niche)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/custom-sections", response_model=list[ProfileCustomSectionOut])
async def list_custom_sections(
    current_user: CurrentUser,
    session: DbSession,
) -> list[ProfileCustomSection]:
    return await _list_section_items(session, ProfileCustomSection, current_user.id)


@router.post(
    "/custom-sections",
    response_model=ProfileCustomSectionOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_custom_section(
    body: ProfileCustomSectionCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileCustomSection:
    profile = await _get_or_create_profile(session, current_user)
    section = ProfileCustomSection(profile_id=profile.id, **body.model_dump())
    session.add(section)
    await session.commit()
    await session.refresh(section)
    return section


@router.get("/custom-sections/{section_id}", response_model=ProfileCustomSectionOut)
async def get_custom_section(
    section_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileCustomSection:
    return await _get_section_item_or_404(
        session, ProfileCustomSection, section_id, current_user.id
    )


@router.patch("/custom-sections/{section_id}", response_model=ProfileCustomSectionOut)
async def update_custom_section(
    section_id: uuid.UUID,
    body: ProfileCustomSectionUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfileCustomSection:
    section = await _get_section_item_or_404(
        session, ProfileCustomSection, section_id, current_user.id
    )
    _apply_updates(section, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(section)
    return section


@router.delete("/custom-sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_section(
    section_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    section = await _get_section_item_or_404(
        session, ProfileCustomSection, section_id, current_user.id
    )
    await session.delete(section)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/preferences", response_model=ProfilePreferencesOut)
async def get_preferences(
    current_user: CurrentUser,
    session: DbSession,
) -> ProfilePreferences:
    profile = await _get_profile_or_404(session, current_user.id, eager=True)
    if profile.preferences is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")
    return profile.preferences


@router.post(
    "/preferences",
    response_model=ProfilePreferencesOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_preferences(
    body: ProfilePreferencesCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfilePreferences:
    profile = await _get_or_create_profile(session, current_user)
    existing = await session.scalar(
        select(ProfilePreferences).where(ProfilePreferences.profile_id == profile.id)
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Preferences already exist",
        )

    preferences = ProfilePreferences(profile_id=profile.id, **body.model_dump())
    session.add(preferences)
    await session.commit()
    await session.refresh(preferences)
    return preferences


@router.patch("/preferences", response_model=ProfilePreferencesOut)
async def update_preferences(
    body: ProfilePreferencesUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProfilePreferences:
    profile = await _get_profile_or_404(session, current_user.id, eager=True)
    if profile.preferences is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

    _apply_updates(profile.preferences, body.model_dump(exclude_unset=True))
    await session.commit()
    await session.refresh(profile.preferences)
    return profile.preferences


@router.delete("/preferences", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preferences(
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    profile = await _get_profile_or_404(session, current_user.id, eager=True)
    if profile.preferences is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

    await session.delete(profile.preferences)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
