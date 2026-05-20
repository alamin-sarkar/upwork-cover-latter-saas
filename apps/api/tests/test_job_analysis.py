import json
import uuid
from types import SimpleNamespace

import pytest
from ai_workflows.job_analysis import JOB_ANALYSIS_PROMPT_VERSION
from fastapi.testclient import TestClient

from app.api.routes import job_analysis as job_analysis_route
from app.core.config import get_settings
from app.main import app
from app.models.job_analysis import JobAnalysisSnapshot
from app.services.job_analysis import JobAnalysisService

client = TestClient(app)


def _email() -> str:
    return f"job-analysis-{uuid.uuid4().hex[:10]}@acme.com"


def _auth_headers() -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={
            "email": _email(),
            "password": "Secret1234",
            "full_name": "Job Analysis Tester",
        },
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class FakeMessagesAPI:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload
        self.calls: list[dict[str, object]] = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=json.dumps(self.payload))]
        )


class FakeAnthropicClient:
    def __init__(self, payload: dict[str, object]) -> None:
        self.messages = FakeMessagesAPI(payload)


ANALYSIS_PAYLOAD = {
    "title": "Senior React Dashboard Engineer",
    "scope": "Build and stabilize a client reporting dashboard for a B2B SaaS team.",
    "deliverables": [
        "Ship a React analytics dashboard",
        "Integrate live reporting APIs",
        "Improve slow table interactions",
    ],
    "required_skills": ["React", "TypeScript", "API integration", "Performance tuning"],
    "budget_clues": [
        "Long-term ownership is preferred",
        "Fast turnaround is mentioned",
        "Senior-level autonomy is implied",
    ],
    "urgency": "high",
    "tone": "demanding",
    "risk_flags": ["Tight timeline", "Ambiguous current API quality"],
    "fit_score": 86,
}


@pytest.mark.asyncio
async def test_job_analysis_returns_structured_snapshot_and_persists(db_session):
    headers = _auth_headers()
    fake_client = FakeAnthropicClient(ANALYSIS_PAYLOAD)

    original_factory = job_analysis_route.get_job_analysis_service
    job_analysis_route.get_job_analysis_service = lambda: JobAnalysisService(
        client=fake_client,
        settings=get_settings(),
    )

    raw_job_text = """
We need a senior React engineer to own a reporting dashboard rebuild.
You should be comfortable with TypeScript, API integrations, and performance tuning.
We have paying enterprise users waiting on better analytics and need fast execution.
""".strip()

    try:
        response = client.post(
            "/jobs/analyze",
            headers=headers,
            json={"raw_job_text": raw_job_text},
        )
    finally:
        job_analysis_route.get_job_analysis_service = original_factory

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == ANALYSIS_PAYLOAD["title"]
    assert body["fit_score"] == 86
    assert body["urgency"] == "high"
    assert body["tone"] == "demanding"
    assert body["prompt_version"] == JOB_ANALYSIS_PROMPT_VERSION
    assert body["provider"] == "anthropic"
    assert body["model_name"] == get_settings().anthropic_model
    assert fake_client.messages.calls[0]["model"] == get_settings().anthropic_model

    snapshot = await db_session.get(JobAnalysisSnapshot, uuid.UUID(body["id"]))
    assert snapshot is not None
    assert snapshot.raw_job_text == raw_job_text
    assert snapshot.analysis_payload["required_skills"] == ANALYSIS_PAYLOAD["required_skills"]
    assert snapshot.fit_score == 86


def test_job_analysis_rejects_too_short_job_posts():
    headers = _auth_headers()

    response = client.post(
        "/jobs/analyze",
        headers=headers,
        json={"raw_job_text": "too short"},
    )

    assert response.status_code == 422
