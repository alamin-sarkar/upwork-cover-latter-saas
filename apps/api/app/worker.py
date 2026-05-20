from __future__ import annotations

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "upwork_cover_letter",
    broker=settings.redis_url,
    backend=settings.celery_result_backend or settings.redis_url,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_default_queue=settings.celery_default_queue,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    task_always_eager=settings.celery_task_always_eager,
)
