import uuid
from typing import Any, TypeVar

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import select

from app.core.deps import CurrentUser, DbSession
from app.models.library import CoverLetterGuideline, CoverLetterSample
from app.schemas.library import (
    CoverLetterGuidelineCreate,
    CoverLetterGuidelineOut,
    CoverLetterGuidelineUpdate,
    CoverLetterSampleCreate,
    CoverLetterSampleOut,
    CoverLetterSampleUpdate,
    GuidelineType,
    SampleTag,
)

router = APIRouter(prefix="/library", tags=["library"])

LibraryModel = TypeVar("LibraryModel", CoverLetterGuideline, CoverLetterSample)


def _apply_updates(instance: Any, updates: dict[str, Any]) -> Any:
    for field, value in updates.items():
        setattr(instance, field, value)
    return instance


async def _get_item_or_404(
    session: DbSession,
    model: type[LibraryModel],
    item_id: uuid.UUID,
    user_id: uuid.UUID,
) -> LibraryModel:
    stmt = select(model).where(model.id == item_id, model.user_id == user_id)
    item = await session.scalar(stmt)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return item


@router.get("/guidelines", response_model=list[CoverLetterGuidelineOut])
async def list_guidelines(
    current_user: CurrentUser,
    session: DbSession,
    guideline_type: GuidelineType | None = Query(default=None),
) -> list[CoverLetterGuideline]:
    stmt = select(CoverLetterGuideline).where(CoverLetterGuideline.user_id == current_user.id)
    if guideline_type is not None:
        stmt = stmt.where(CoverLetterGuideline.guideline_type == guideline_type.value)
    stmt = stmt.order_by(
        CoverLetterGuideline.sort_order.asc(), CoverLetterGuideline.created_at.asc()
    )
    return list(await session.scalars(stmt))


@router.post(
    "/guidelines",
    response_model=CoverLetterGuidelineOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_guideline(
    body: CoverLetterGuidelineCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterGuideline:
    guideline = CoverLetterGuideline(user_id=current_user.id, **body.model_dump(mode="json"))
    session.add(guideline)
    await session.commit()
    await session.refresh(guideline)
    return guideline


@router.get("/guidelines/{guideline_id}", response_model=CoverLetterGuidelineOut)
async def get_guideline(
    guideline_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterGuideline:
    return await _get_item_or_404(session, CoverLetterGuideline, guideline_id, current_user.id)


@router.patch("/guidelines/{guideline_id}", response_model=CoverLetterGuidelineOut)
async def update_guideline(
    guideline_id: uuid.UUID,
    body: CoverLetterGuidelineUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterGuideline:
    guideline = await _get_item_or_404(
        session, CoverLetterGuideline, guideline_id, current_user.id
    )
    _apply_updates(guideline, body.model_dump(exclude_unset=True, mode="json"))
    await session.commit()
    await session.refresh(guideline)
    return guideline


@router.delete("/guidelines/{guideline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guideline(
    guideline_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    guideline = await _get_item_or_404(
        session, CoverLetterGuideline, guideline_id, current_user.id
    )
    await session.delete(guideline)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/samples", response_model=list[CoverLetterSampleOut])
async def list_samples(
    current_user: CurrentUser,
    session: DbSession,
    tag: SampleTag | None = Query(default=None),
) -> list[CoverLetterSample]:
    stmt = select(CoverLetterSample).where(CoverLetterSample.user_id == current_user.id)
    if tag is not None:
        stmt = stmt.where(CoverLetterSample.tag == tag.value)
    stmt = stmt.order_by(CoverLetterSample.sort_order.asc(), CoverLetterSample.created_at.asc())
    return list(await session.scalars(stmt))


@router.post(
    "/samples",
    response_model=CoverLetterSampleOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_sample(
    body: CoverLetterSampleCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterSample:
    sample = CoverLetterSample(user_id=current_user.id, **body.model_dump(mode="json"))
    session.add(sample)
    await session.commit()
    await session.refresh(sample)
    return sample


@router.get("/samples/{sample_id}", response_model=CoverLetterSampleOut)
async def get_sample(
    sample_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterSample:
    return await _get_item_or_404(session, CoverLetterSample, sample_id, current_user.id)


@router.patch("/samples/{sample_id}", response_model=CoverLetterSampleOut)
async def update_sample(
    sample_id: uuid.UUID,
    body: CoverLetterSampleUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterSample:
    sample = await _get_item_or_404(session, CoverLetterSample, sample_id, current_user.id)
    _apply_updates(sample, body.model_dump(exclude_unset=True, mode="json"))
    await session.commit()
    await session.refresh(sample)
    return sample


@router.delete("/samples/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sample(
    sample_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    sample = await _get_item_or_404(session, CoverLetterSample, sample_id, current_user.id)
    await session.delete(sample)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
