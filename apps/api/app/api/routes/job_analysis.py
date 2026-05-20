from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.job_analysis import JobAnalysisRequest, JobAnalysisResponse
from app.services.job_analysis import (
    JobAnalysisConfigurationError,
    get_job_analysis_service,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/analyze", response_model=JobAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_job_post(
    body: JobAnalysisRequest,
    current_user: CurrentUser,
    session: DbSession,
):
    try:
        service = get_job_analysis_service()
    except JobAnalysisConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Job analysis provider is not configured",
        ) from exc

    return await service.analyze_job_post(
        user_id=current_user.id,
        raw_job_text=body.raw_job_text,
        session=session,
    )
