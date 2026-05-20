from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request, status

from app.core.config import get_settings
from app.core.health import check_celery_workers, check_database, check_redis

router = APIRouter(prefix="/admin", tags=["admin"])


def _require_admin_token(x_admin_token: str | None) -> None:
    settings = get_settings()
    if not settings.admin_diagnostics_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin diagnostics token is not configured",
        )
    if x_admin_token != settings.admin_diagnostics_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin token")


@router.get("/diagnostics")
async def diagnostics(
    request: Request,
    x_admin_token: str | None = Header(default=None),
):
    _require_admin_token(x_admin_token)
    settings = get_settings()
    database = await check_database()
    redis = await check_redis()
    celery = await check_celery_workers()

    return {
        "app": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        },
        "request_id": getattr(request.state, "request_id", None),
        "dependencies": {
            "database": database,
            "redis": redis,
            "celery": celery,
        },
        "rate_limits": {
            "job_analysis_daily_limits": settings.job_analysis_daily_limits,
            "generation_daily_limits": settings.generation_daily_limits,
            "window_seconds": settings.rate_limit_window_seconds,
        },
        "celery": {
            "default_queue": settings.celery_default_queue,
            "result_backend": settings.celery_result_backend or settings.redis_url,
            "task_always_eager": settings.celery_task_always_eager,
        },
    }
