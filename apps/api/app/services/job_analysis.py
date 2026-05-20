from __future__ import annotations

import json
import re
import uuid
from collections.abc import Sequence
from typing import Any

from ai_workflows.job_analysis import (
    JOB_ANALYSIS_PROMPT_VERSION,
    JobAnalysis,
    build_job_analysis_graph,
    build_job_analysis_prompt,
)
from ai_workflows.job_analysis.prompts import JOB_ANALYSIS_SYSTEM_PROMPT
from anthropic import AsyncAnthropic
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.models.job_analysis import JobAnalysisSnapshot


class JobAnalysisService:
    def __init__(
        self,
        *,
        client: Any | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        if client is None and not self.settings.anthropic_api_key:
            raise JobAnalysisConfigurationError("Anthropic API key is not configured")
        self.client = client or AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        self.graph = build_job_analysis_graph(self._analyze_with_model)

    async def analyze_job_post(
        self,
        *,
        user_id: uuid.UUID,
        raw_job_text: str,
        session: AsyncSession,
    ) -> JobAnalysisSnapshot:
        state = await self.graph.ainvoke({"raw_job_text": raw_job_text})
        analysis = state["analysis"]

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
            provider="anthropic",
            model_name=self.settings.anthropic_model,
            prompt_version=JOB_ANALYSIS_PROMPT_VERSION,
        )
        session.add(snapshot)
        await session.commit()
        await session.refresh(snapshot)
        return snapshot

    async def _analyze_with_model(self, raw_job_text: str) -> JobAnalysis:
        response = await self.client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=1200,
            temperature=0,
            system=JOB_ANALYSIS_PROMPT_VERSION + "\n\n" + JOB_ANALYSIS_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_job_analysis_prompt(raw_job_text)}],
        )
        text = _extract_text_blocks(response.content)
        json_blob = _extract_json_blob(text)
        return JobAnalysis.model_validate_json(json_blob)


def get_job_analysis_service() -> JobAnalysisService:
    return JobAnalysisService()


class JobAnalysisConfigurationError(RuntimeError):
    pass


def _extract_text_blocks(content_blocks: Sequence[Any]) -> str:
    parts: list[str] = []
    for block in content_blocks:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    if not parts:
        raise ValueError("Anthropic response did not include text content")
    return "\n".join(parts).strip()


def _extract_json_blob(text: str) -> str:
    fenced_match = re.search(r"```json\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)

    try:
        json.loads(text)
    except json.JSONDecodeError:
        object_match = re.search(r"(\{.*\})", text, re.DOTALL)
        if not object_match:
            raise ValueError("Model response did not contain a JSON object") from None
        return object_match.group(1)
    return text
