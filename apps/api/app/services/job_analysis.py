from __future__ import annotations

import json
import re
import uuid
from typing import Any

from ai_workflows.job_analysis import (
    JOB_ANALYSIS_PROMPT_VERSION,
    JobAnalysis,
    build_job_analysis_graph,
    build_job_analysis_prompt,
)
from ai_workflows.job_analysis.prompts import JOB_ANALYSIS_SYSTEM_PROMPT
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.llm_provider import raw_completion
from app.models.job_analysis import JobAnalysisSnapshot


class JobAnalysisService:
    def __init__(
        self,
        *,
        settings: Settings | None = None,
        # Test injection: async callable (raw_job_text) -> JobAnalysis
        analyzer_override: Any | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._analyzer_override = analyzer_override
        self.graph = build_job_analysis_graph(self._analyze_with_model)

    async def analyze_job_post(
        self,
        *,
        user_id: uuid.UUID,
        raw_job_text: str,
        session: AsyncSession,
    ) -> JobAnalysisSnapshot:
        state = await self.graph.ainvoke({"raw_job_text": raw_job_text})
        analysis: JobAnalysis = state["analysis"]

        snapshot = JobAnalysisSnapshot(
            user_id=user_id,
            raw_job_text=raw_job_text,
            title=analysis.title,
            scope=analysis.scope,
            deliverables=analysis.deliverables,
            required_skills=analysis.required_skills,
            budget_clues=analysis.budget_clues,
            urgency=analysis.urgency.value,
            tone=analysis.tone.value,
            risk_flags=analysis.risk_flags,
            fit_score=analysis.fit_score,
            analysis_payload=analysis.model_dump(mode="json"),
            provider=self.settings.llm_provider,
            model_name=self._active_model_name(),
            prompt_version=JOB_ANALYSIS_PROMPT_VERSION,
        )
        session.add(snapshot)
        await session.commit()
        await session.refresh(snapshot)
        return snapshot

    async def _analyze_with_model(self, raw_job_text: str) -> JobAnalysis:
        if self._analyzer_override is not None:
            return await self._analyzer_override(raw_job_text)

        system = (
            JOB_ANALYSIS_PROMPT_VERSION + "\n\n" + JOB_ANALYSIS_SYSTEM_PROMPT
        )
        messages = [
            {"role": "user", "content": build_job_analysis_prompt(raw_job_text)}
        ]
        text = await raw_completion(
            messages, system=system, max_tokens=1200, settings=self.settings
        )
        return JobAnalysis.model_validate_json(_extract_json_blob(text))

    def _active_model_name(self) -> str:
        if self.settings.llm_provider == "anthropic":
            return self.settings.anthropic_model
        return self.settings.local_llm_model


def get_job_analysis_service() -> JobAnalysisService:
    return JobAnalysisService()


class JobAnalysisConfigurationError(RuntimeError):
    pass


def _extract_json_blob(text: str) -> str:
    fenced = re.search(r"```json\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        return fenced.group(1)
    try:
        json.loads(text)
    except json.JSONDecodeError:
        obj = re.search(r"(\{.*\})", text, re.DOTALL)
        if not obj:
            raise ValueError(
                "Model response did not contain a JSON object"
            ) from None
        return obj.group(1)
    return text
