from __future__ import annotations

import asyncio
import uuid
from typing import Any

from ai_workflows.generation.schemas import CoverLetterStructure

from app.core.db import SessionLocal
from app.services.generation import get_cover_letter_generation_service
from app.services.job_analysis import get_job_analysis_service
from app.worker import celery_app


@celery_app.task(name="pitchcraft.job_analysis.analyze_post")
def analyze_job_post_task(user_id: str, raw_job_text: str) -> dict[str, Any]:
    return asyncio.run(_analyze_job_post(user_id=user_id, raw_job_text=raw_job_text))


async def _analyze_job_post(*, user_id: str, raw_job_text: str) -> dict[str, Any]:
    async with SessionLocal() as session:
        snapshot = await get_job_analysis_service().analyze_job_post(
            user_id=uuid.UUID(user_id),
            raw_job_text=raw_job_text,
            session=session,
        )
        return {
            "analysis_snapshot_id": str(snapshot.id),
            "title": snapshot.title,
            "fit_score": snapshot.fit_score,
        }


@celery_app.task(name="pitchcraft.cover_letters.generate")
def generate_cover_letters_task(
    user_id: str,
    raw_job_text: str | None = None,
    analysis_snapshot_id: str | None = None,
    structures: list[str] | None = None,
) -> dict[str, Any]:
    return asyncio.run(
        _generate_cover_letters(
            user_id=user_id,
            raw_job_text=raw_job_text,
            analysis_snapshot_id=analysis_snapshot_id,
            structures=structures,
        )
    )


async def _generate_cover_letters(
    *,
    user_id: str,
    raw_job_text: str | None,
    analysis_snapshot_id: str | None,
    structures: list[str] | None,
) -> dict[str, Any]:
    parsed_structures = [CoverLetterStructure(item) for item in structures] if structures else None
    async with SessionLocal() as session:
        run = await get_cover_letter_generation_service().generate_cover_letters(
            user_id=uuid.UUID(user_id),
            session=session,
            raw_job_text=raw_job_text,
            analysis_snapshot_id=uuid.UUID(analysis_snapshot_id) if analysis_snapshot_id else None,
            structures=parsed_structures,
        )
        return {
            "generation_run_id": str(run.id),
            "analysis_snapshot_id": str(run.analysis_snapshot_id),
            "variant_ids": [str(item.id) for item in run.variants],
        }


@celery_app.task(name="pitchcraft.worker.ping")
def ping_task() -> dict[str, str]:
    return {"status": "ok"}
