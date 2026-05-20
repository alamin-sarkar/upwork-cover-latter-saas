from __future__ import annotations

import hashlib
import math
import re
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.feedback import CoverLetterFeedback, FEEDBACK_EMBEDDING_DIMENSIONS
from app.models.generation import CoverLetterGenerationVariant

TOKEN_RE = re.compile(r"[a-z0-9]{2,}", re.IGNORECASE)


def build_feedback_memory_text(
    *,
    variant: CoverLetterGenerationVariant,
    rating: int,
    edited_cover_letter: str | None,
    accepted_sections: list[str],
    rejected_sections: list[str],
    client_response_outcome: str,
    notes: str | None,
) -> str:
    parts = [
        f"Structure: {variant.structure}",
        f"Headline: {variant.headline}",
        f"Rating: {rating}/5",
        f"Client outcome: {client_response_outcome}",
        f"Original rationale: {variant.rationale}",
    ]
    if accepted_sections:
        parts.append("Accepted sections: " + " | ".join(accepted_sections))
    if rejected_sections:
        parts.append("Rejected sections: " + " | ".join(rejected_sections))
    if edited_cover_letter:
        parts.append("Edited final text: " + edited_cover_letter)
    else:
        parts.append("Original cover letter: " + variant.cover_letter)
    if notes:
        parts.append("Notes: " + notes)
    return "\n".join(parts)


def embed_text(text: str, *, dimensions: int = FEEDBACK_EMBEDDING_DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    for token in TOKEN_RE.findall(text.lower()):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
        bucket = int.from_bytes(digest[:8], "big") % dimensions
        sign = 1.0 if digest[8] % 2 == 0 else -1.0
        weight = 1.5 if len(token) > 6 else 1.0
        vector[bucket] += sign * weight

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


async def get_owned_variant(
    *,
    session: AsyncSession,
    user_id: uuid.UUID,
    generation_variant_id: uuid.UUID,
) -> CoverLetterGenerationVariant | None:
    stmt = (
        select(CoverLetterGenerationVariant)
        .join(CoverLetterGenerationVariant.generation_run)
        .where(
            CoverLetterGenerationVariant.id == generation_variant_id,
            CoverLetterGenerationVariant.generation_run.has(user_id=user_id),
        )
        .options(joinedload(CoverLetterGenerationVariant.generation_run))
    )
    return await session.scalar(stmt)


async def retrieve_feedback_memory_context(
    *,
    session: AsyncSession,
    user_id: uuid.UUID,
    query_text: str,
    limit: int = 3,
) -> str:
    embedding = embed_text(query_text)
    stmt = (
        select(CoverLetterFeedback)
        .where(CoverLetterFeedback.user_id == user_id)
        .order_by(CoverLetterFeedback.memory_embedding.cosine_distance(embedding))
        .limit(limit)
    )
    feedback_items = list(await session.scalars(stmt))
    if not feedback_items:
        return "No past feedback memory is available yet."

    parts = []
    for item in feedback_items:
        parts.append(
            "\n".join(
                [
                    f"Feedback memory #{item.id}:",
                    f"- Rating: {item.rating}/5",
                    f"- Client outcome: {item.client_response_outcome}",
                    f"- Accepted sections: {' | '.join(item.accepted_sections) if item.accepted_sections else 'n/a'}",
                    f"- Rejected sections: {' | '.join(item.rejected_sections) if item.rejected_sections else 'n/a'}",
                    f"- Edited text: {item.edited_cover_letter or 'n/a'}",
                    f"- Notes: {item.notes or 'n/a'}",
                ]
            )
        )
    return "\n\n".join(parts)
