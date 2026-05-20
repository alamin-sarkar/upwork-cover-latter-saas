from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.generation import CoverLetterGenerateRequest, CoverLetterGenerationResponse
from app.services.generation import GenerationNotFoundError, get_cover_letter_generation_service
from app.services.job_analysis import JobAnalysisConfigurationError

router = APIRouter(tags=["generation"])


@router.post("/generate", response_model=CoverLetterGenerationResponse, status_code=status.HTTP_201_CREATED)
async def generate_cover_letters(
    body: CoverLetterGenerateRequest,
    current_user: CurrentUser,
    session: DbSession,
):
    try:
        service = get_cover_letter_generation_service()
    except JobAnalysisConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cover letter generation provider is not configured",
        ) from exc

    try:
        run = await service.generate_cover_letters(
            user_id=current_user.id,
            session=session,
            raw_job_text=body.raw_job_text,
            analysis_snapshot_id=body.analysis_snapshot_id,
            structures=body.structures,
        )
    except GenerationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return {
        "id": run.id,
        "analysis_snapshot_id": run.analysis_snapshot_id,
        "raw_job_text": run.raw_job_text,
        "prompt_version": run.prompt_version,
        "requested_structures": run.requested_structures,
        "analysis": run.analysis_snapshot.analysis_payload,
        "variants": run.variants,
        "created_at": run.created_at,
    }
