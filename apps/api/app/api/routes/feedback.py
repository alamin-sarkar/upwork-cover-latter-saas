import uuid

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.core.deps import CurrentUser, DbSession
from app.models.feedback import CoverLetterFeedback
from app.schemas.feedback import (
    ClientResponseOutcome,
    CoverLetterFeedbackCreate,
    CoverLetterFeedbackOut,
    CoverLetterFeedbackUpdate,
)
from app.services.feedback_memory import (
    build_feedback_memory_text,
    embed_text,
    get_owned_variant,
)

router = APIRouter(prefix="/history", tags=["history"])


async def _get_feedback_or_404(
    *,
    session: DbSession,
    user_id: uuid.UUID,
    feedback_id: uuid.UUID,
) -> CoverLetterFeedback:
    stmt = select(CoverLetterFeedback).where(
        CoverLetterFeedback.id == feedback_id,
        CoverLetterFeedback.user_id == user_id,
    )
    feedback = await session.scalar(stmt)
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return feedback


@router.get("/feedback", response_model=list[CoverLetterFeedbackOut])
async def list_feedback(
    current_user: CurrentUser,
    session: DbSession,
    generation_run_id: uuid.UUID | None = Query(default=None),
    client_response_outcome: ClientResponseOutcome | None = Query(default=None),
) -> list[CoverLetterFeedback]:
    stmt = select(CoverLetterFeedback).where(CoverLetterFeedback.user_id == current_user.id)
    if generation_run_id is not None:
        stmt = stmt.where(CoverLetterFeedback.generation_run_id == generation_run_id)
    if client_response_outcome is not None:
        stmt = stmt.where(
            CoverLetterFeedback.client_response_outcome == client_response_outcome.value
        )
    stmt = stmt.order_by(CoverLetterFeedback.created_at.desc())
    return list(await session.scalars(stmt))


@router.post("/feedback", response_model=CoverLetterFeedbackOut, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    body: CoverLetterFeedbackCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterFeedback:
    variant = await get_owned_variant(
        session=session,
        user_id=current_user.id,
        generation_variant_id=body.generation_variant_id,
    )
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found")
    existing_feedback = await session.scalar(
        select(CoverLetterFeedback).where(
            CoverLetterFeedback.generation_variant_id == variant.id,
            CoverLetterFeedback.user_id == current_user.id,
        )
    )
    if existing_feedback is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feedback already exists for this variant",
        )

    memory_text = build_feedback_memory_text(
        variant=variant,
        rating=body.rating,
        edited_cover_letter=body.edited_cover_letter,
        accepted_sections=body.accepted_sections,
        rejected_sections=body.rejected_sections,
        client_response_outcome=body.client_response_outcome.value,
        notes=body.notes,
    )
    feedback = CoverLetterFeedback(
        user_id=current_user.id,
        generation_run_id=variant.generation_run_id,
        generation_variant_id=variant.id,
        rating=body.rating,
        edited_cover_letter=body.edited_cover_letter,
        accepted_sections=body.accepted_sections,
        rejected_sections=body.rejected_sections,
        client_response_outcome=body.client_response_outcome.value,
        notes=body.notes,
        memory_text=memory_text,
        memory_embedding=embed_text(memory_text),
    )
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback


@router.get("/feedback/{feedback_id}", response_model=CoverLetterFeedbackOut)
async def get_feedback(
    feedback_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterFeedback:
    return await _get_feedback_or_404(
        session=session,
        user_id=current_user.id,
        feedback_id=feedback_id,
    )


@router.patch("/feedback/{feedback_id}", response_model=CoverLetterFeedbackOut)
async def update_feedback(
    feedback_id: uuid.UUID,
    body: CoverLetterFeedbackUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> CoverLetterFeedback:
    feedback = await _get_feedback_or_404(
        session=session,
        user_id=current_user.id,
        feedback_id=feedback_id,
    )
    updates = body.model_dump(exclude_unset=True, mode="json")
    for field, value in updates.items():
        setattr(feedback, field, value)

    variant = await get_owned_variant(
        session=session,
        user_id=current_user.id,
        generation_variant_id=feedback.generation_variant_id,
    )
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found")

    feedback.memory_text = build_feedback_memory_text(
        variant=variant,
        rating=feedback.rating,
        edited_cover_letter=feedback.edited_cover_letter,
        accepted_sections=feedback.accepted_sections,
        rejected_sections=feedback.rejected_sections,
        client_response_outcome=feedback.client_response_outcome,
        notes=feedback.notes,
    )
    feedback.memory_embedding = embed_text(feedback.memory_text)
    await session.commit()
    await session.refresh(feedback)
    return feedback
