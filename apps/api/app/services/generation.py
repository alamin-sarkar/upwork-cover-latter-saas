from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from ai_workflows.generation import (
    COVER_LETTER_GENERATION_PROMPT_VERSION,
    COVER_LETTER_REVIEW_PROMPT_VERSION,
    CoverLetterReviewResult,
    CoverLetterStructure,
    DraftedCoverLetter,
    FinalCoverLetterVariant,
    build_cover_letter_draft_prompt,
    build_cover_letter_generation_graph,
    build_cover_letter_review_prompt,
)
from ai_workflows.job_analysis import JobAnalysis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import Settings, get_settings
from app.core.llm_provider import langchain_chat_model, structured_output_method
from app.models.generation import (
    CoverLetterGenerationRun,
    CoverLetterGenerationVariant,
)
from app.models.job_analysis import JobAnalysisSnapshot
from app.models.library import CoverLetterGuideline, CoverLetterSample
from app.models.profile import Profile
from app.services.feedback_memory import retrieve_feedback_memory_context
from app.services.job_analysis import JobAnalysisService

StructuredInvoker = Callable[[type[Any]], Any]


class CoverLetterGenerationService:
    def __init__(
        self,
        *,
        draft_model_factory: StructuredInvoker | None = None,
        review_model_factory: StructuredInvoker | None = None,
        job_analysis_service: JobAnalysisService | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()

        if draft_model_factory is None or review_model_factory is None:
            base_model = langchain_chat_model(self.settings)
            method = structured_output_method(self.settings)
            default_factory: StructuredInvoker = (
                lambda schema, _m=base_model, _mt=method: (
                    _m.with_structured_output(schema, method=_mt)
                )
            )
        else:
            default_factory = None  # type: ignore[assignment]

        self.draft_model_factory = draft_model_factory or default_factory
        self.review_model_factory = review_model_factory or default_factory
        self.job_analysis_service = job_analysis_service
        self.graph = build_cover_letter_generation_graph(
            analyze_job=self._analyze_job,
            retrieve_profile=self._retrieve_profile,
            retrieve_library=self._retrieve_library,
            retrieve_feedback_memory=self._retrieve_feedback_memory,
            draft_variants=self._draft_variants,
            review_variants=self._review_variants,
        )
        self._session: AsyncSession | None = None
        self._user_id: uuid.UUID | None = None

    async def generate_cover_letters(
        self,
        *,
        user_id: uuid.UUID,
        session: AsyncSession,
        raw_job_text: str | None = None,
        analysis_snapshot_id: uuid.UUID | None = None,
        structures: list[CoverLetterStructure] | None = None,
    ) -> CoverLetterGenerationRun:
        self._session = session
        self._user_id = user_id

        initial_state: dict[str, object] = {
            "raw_job_text": raw_job_text,
            "analysis_snapshot_id": str(analysis_snapshot_id) if analysis_snapshot_id else None,
            "analysis": None,
            "requested_structures": [item.value for item in structures] if structures else None,
            "profile_context": None,
            "library_context": None,
            "feedback_memory_context": None,
            "drafted_variants": None,
            "final_variants": None,
        }

        if analysis_snapshot_id:
            snapshot = await self._get_analysis_snapshot(analysis_snapshot_id)
            initial_state["raw_job_text"] = snapshot.raw_job_text
            initial_state["analysis"] = JobAnalysis.model_validate(snapshot.analysis_payload)

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        state = await self.graph.ainvoke(initial_state, config=config)
        graph_state = await self.graph.aget_state(config)

        analysis_snapshot = await self._get_analysis_snapshot(
            uuid.UUID(state["analysis_snapshot_id"])
        )
        run = CoverLetterGenerationRun(
            user_id=user_id,
            analysis_snapshot_id=analysis_snapshot.id,
            raw_job_text=analysis_snapshot.raw_job_text,
            requested_structures=state["requested_structures"],
            prompt_version=COVER_LETTER_GENERATION_PROMPT_VERSION,
            graph_state=_serialize_graph_state(graph_state.values),
        )

        for index, variant in enumerate(state["final_variants"]):
            run.variants.append(
                CoverLetterGenerationVariant(
                    structure=variant.structure.value,
                    headline=variant.headline,
                    cover_letter=variant.cover_letter,
                    rationale=variant.rationale,
                    match_notes=variant.match_notes,
                    self_check_notes=variant.self_check_notes,
                    sort_order=index,
                )
            )

        session.add(run)
        await session.commit()
        await session.refresh(run)
        await session.refresh(run, attribute_names=["variants", "analysis_snapshot"])
        return run

    async def _analyze_job(self, state: dict[str, object]) -> dict[str, object]:
        if state.get("analysis") is not None and state.get("analysis_snapshot_id") is not None:
            return {}

        raw_job_text = state["raw_job_text"]
        analysis_service = self.job_analysis_service or JobAnalysisService(settings=self.settings)
        snapshot = await analysis_service.analyze_job_post(
            user_id=self._require_user_id(),
            raw_job_text=raw_job_text,
            session=self._require_session(),
        )
        return {
            "analysis": JobAnalysis.model_validate(snapshot.analysis_payload),
            "analysis_snapshot_id": str(snapshot.id),
            "raw_job_text": snapshot.raw_job_text,
        }

    async def _retrieve_profile(self, state: dict[str, object]) -> dict[str, str]:
        stmt = (
            select(Profile)
            .where(Profile.user_id == self._require_user_id())
            .options(
                selectinload(Profile.skills),
                selectinload(Profile.projects),
                selectinload(Profile.experiences),
                selectinload(Profile.niches),
                selectinload(Profile.custom_sections),
                selectinload(Profile.preferences),
            )
        )
        profile = await self._require_session().scalar(stmt)
        if profile is None:
            return {"profile_context": "No structured profile is configured yet."}

        parts = [
            f"Professional title: {profile.professional_title or 'N/A'}",
            f"About: {profile.about or 'N/A'}",
            f"Availability: {profile.availability_note or 'N/A'}",
        ]
        if profile.preferences is not None:
            parts.extend(
                [
                    f"Preferred tone: {profile.preferences.default_tone or 'N/A'}",
                    f"Voice note: {profile.preferences.voice_note or 'N/A'}",
                    f"CTA style: {profile.preferences.cta_style or 'N/A'}",
                ]
            )
        if profile.skills:
            parts.append(
                "Skills: "
                + "; ".join(
                    f"{item.name} ({item.level or 'unspecified'}; proof: {item.proof or 'n/a'})"
                    for item in profile.skills
                )
            )
        if profile.projects:
            parts.append(
                "Projects: "
                + "; ".join(
                    f"{item.title}: {item.description} | outcome: {item.outcome or 'n/a'}"
                    for item in profile.projects
                )
            )
        if profile.experiences:
            parts.append(
                "Experience: "
                + "; ".join(
                    f"{item.role} at {item.company}: {item.summary or 'n/a'}"
                    for item in profile.experiences
                )
            )
        if profile.niches:
            parts.append(
                "Niches: " + "; ".join(f"{item.name}: {item.summary or 'n/a'}" for item in profile.niches)
            )
        if profile.custom_sections:
            parts.append(
                "Custom sections: "
                + "; ".join(f"{item.title}: {item.content}" for item in profile.custom_sections)
            )
        return {"profile_context": "\n".join(parts)}

    async def _retrieve_library(self, state: dict[str, object]) -> dict[str, str]:
        session = self._require_session()
        user_id = self._require_user_id()
        guidelines = list(
            await session.scalars(
                select(CoverLetterGuideline)
                .where(CoverLetterGuideline.user_id == user_id)
                .order_by(CoverLetterGuideline.sort_order.asc(), CoverLetterGuideline.created_at.asc())
            )
        )
        samples = list(
            await session.scalars(
                select(CoverLetterSample)
                .where(CoverLetterSample.user_id == user_id)
                .order_by(CoverLetterSample.sort_order.asc(), CoverLetterSample.created_at.asc())
            )
        )

        parts: list[str] = []
        if guidelines:
            parts.append(
                "Guidelines: "
                + "; ".join(
                    f"[{item.guideline_type}] {item.title}: {item.content}" for item in guidelines
                )
            )
        if samples:
            parts.append(
                "Samples: "
                + "; ".join(
                    f"[{item.tag}] {item.title}: {item.notes or item.outcome or item.content[:160]}"
                    for item in samples
                )
            )
        if not parts:
            parts.append("No saved guidelines or samples are configured yet.")
        return {"library_context": "\n".join(parts)}

    async def _draft_variants(
        self,
        state: dict[str, object],
    ) -> dict[str, list[DraftedCoverLetter]]:
        analysis = state["analysis"]
        profile_context = state["profile_context"]
        library_context = state["library_context"]
        feedback_memory_context = state["feedback_memory_context"]

        drafted_variants: list[DraftedCoverLetter] = []
        for structure_value in state["requested_structures"]:
            structure = CoverLetterStructure(structure_value)
            prompt = build_cover_letter_draft_prompt(
                structure=structure,
                job_analysis=analysis,
                profile_context=profile_context,
                library_context=library_context,
                feedback_memory_context=feedback_memory_context,
            )
            messages = await prompt.aformat_messages()
            drafted = await self.draft_model_factory(DraftedCoverLetter).ainvoke(messages)
            drafted_variants.append(drafted)

        return {"drafted_variants": drafted_variants}

    async def _review_variants(
        self,
        state: dict[str, object],
    ) -> dict[str, list[FinalCoverLetterVariant]]:
        analysis = state["analysis"]
        profile_context = state["profile_context"]
        library_context = state["library_context"]
        feedback_memory_context = state["feedback_memory_context"]
        final_variants: list[FinalCoverLetterVariant] = []

        for drafted_variant in state["drafted_variants"]:
            prompt = build_cover_letter_review_prompt(
                drafted_variant_json=drafted_variant.model_dump_json(indent=2),
                job_analysis=analysis,
                profile_context=profile_context,
                library_context=library_context,
                feedback_memory_context=feedback_memory_context,
            )
            messages = await prompt.aformat_messages()
            reviewed = await self.review_model_factory(CoverLetterReviewResult).ainvoke(messages)
            final_variants.append(
                FinalCoverLetterVariant(
                    structure=reviewed.structure,
                    headline=reviewed.final_headline,
                    cover_letter=reviewed.final_cover_letter,
                    rationale=reviewed.final_rationale,
                    match_notes=reviewed.final_match_notes,
                    self_check_notes=reviewed.self_check_notes,
                )
            )

        return {"final_variants": final_variants}

    async def _retrieve_feedback_memory(self, state: dict[str, object]) -> dict[str, str]:
        analysis = state["analysis"]
        query_text = "\n".join(
            [
                state["raw_job_text"] or "",
                analysis.title,
                analysis.scope,
                " ".join(analysis.required_skills),
            ]
        )
        return {
            "feedback_memory_context": await retrieve_feedback_memory_context(
                session=self._require_session(),
                user_id=self._require_user_id(),
                query_text=query_text,
            )
        }

    async def _get_analysis_snapshot(self, snapshot_id: uuid.UUID) -> JobAnalysisSnapshot:
        stmt = select(JobAnalysisSnapshot).where(
            JobAnalysisSnapshot.id == snapshot_id,
            JobAnalysisSnapshot.user_id == self._require_user_id(),
        )
        snapshot = await self._require_session().scalar(stmt)
        if snapshot is None:
            raise GenerationNotFoundError("Analysis snapshot not found")
        return snapshot

    def _require_session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("Session not bound to generation service")
        return self._session

    def _require_user_id(self) -> uuid.UUID:
        if self._user_id is None:
            raise RuntimeError("User not bound to generation service")
        return self._user_id


def get_cover_letter_generation_service() -> CoverLetterGenerationService:
    return CoverLetterGenerationService()


class GenerationNotFoundError(ValueError):
    pass


def _serialize_graph_state(state: dict[str, object]) -> dict[str, object]:
    payload: dict[str, object] = {}
    for key, value in state.items():
        if isinstance(value, list):
            payload[key] = [
                item.model_dump(mode="json") if hasattr(item, "model_dump") else item for item in value
            ]
        elif hasattr(value, "model_dump"):
            payload[key] = value.model_dump(mode="json")
        else:
            payload[key] = value
    payload["review_prompt_version"] = COVER_LETTER_REVIEW_PROMPT_VERSION
    return payload
