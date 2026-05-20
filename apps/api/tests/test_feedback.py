import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.feedback import CoverLetterFeedback
from app.models.generation import CoverLetterGenerationRun, CoverLetterGenerationVariant
from app.models.job_analysis import JobAnalysisSnapshot

client = TestClient(app)


def _email() -> str:
    return f"feedback-{uuid.uuid4().hex[:10]}@acme.com"


def _register_user() -> tuple[dict[str, str], uuid.UUID]:
    response = client.post(
        "/auth/register",
        json={
            "email": _email(),
            "password": "Secret1234",
            "full_name": "Feedback Tester",
        },
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/auth/me", headers=headers)
    assert me_response.status_code == 200
    return headers, uuid.UUID(me_response.json()["id"])


async def _seed_generation_history(db_session, user_id: uuid.UUID) -> CoverLetterGenerationVariant:
    snapshot = JobAnalysisSnapshot(
        user_id=user_id,
        raw_job_text="Need a React dashboard engineer for a SaaS analytics product.",
        title="React dashboard engineer",
        scope="Rebuild a B2B SaaS reporting dashboard.",
        deliverables=["Dashboard rebuild"],
        required_skills=["React", "TypeScript"],
        budget_clues=["Senior ownership"],
        urgency="high",
        tone="demanding",
        risk_flags=["Fast timeline"],
        fit_score=87,
        analysis_payload={
            "title": "React dashboard engineer",
            "scope": "Rebuild a B2B SaaS reporting dashboard.",
            "deliverables": ["Dashboard rebuild"],
            "required_skills": ["React", "TypeScript"],
            "budget_clues": ["Senior ownership"],
            "urgency": "high",
            "tone": "demanding",
            "risk_flags": ["Fast timeline"],
            "fit_score": 87,
        },
        provider="anthropic",
        model_name="claude-test",
        prompt_version="test-analysis",
    )
    run = CoverLetterGenerationRun(
        user_id=user_id,
        analysis_snapshot=snapshot,
        raw_job_text=snapshot.raw_job_text,
        requested_structures=["concise"],
        prompt_version="phase-7-test",
        graph_state={},
    )
    variant = CoverLetterGenerationVariant(
        structure="concise",
        headline="Direct React dashboard fit",
        cover_letter="I have rebuilt reporting dashboards for SaaS products and can stabilize this one fast.",
        rationale="Direct fit for urgent React work.",
        match_notes=["React dashboard experience"],
        self_check_notes=[],
        sort_order=0,
    )
    run.variants.append(variant)
    db_session.add(run)
    await db_session.commit()
    await db_session.refresh(variant)
    return variant


@pytest.mark.asyncio
async def test_feedback_crud_persists_memory_and_enforces_ownership(db_session):
    headers, user_id = _register_user()
    variant = await _seed_generation_history(db_session, user_id)

    create_response = client.post(
        "/history/feedback",
        headers=headers,
        json={
            "generation_variant_id": str(variant.id),
            "rating": 5,
            "edited_cover_letter": "Lead with the reporting pain, then name the exact dashboard outcome.",
            "accepted_sections": ["Lead with the reporting bottleneck"],
            "rejected_sections": ["Do not say passionate"],
            "client_response_outcome": "interview",
            "notes": "Specific KPI proof worked better than generic excitement.",
        },
    )

    assert create_response.status_code == 201
    body = create_response.json()
    assert body["generation_run_id"] == str(variant.generation_run_id)
    assert "Lead with the reporting bottleneck" in body["memory_text"]
    assert body["client_response_outcome"] == "interview"

    feedback = await db_session.get(CoverLetterFeedback, uuid.UUID(body["id"]))
    assert feedback is not None
    assert len(feedback.memory_embedding) == 256

    list_response = client.get("/history/feedback", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/history/feedback/{body['id']}",
        headers=headers,
        json={
            "client_response_outcome": "hired",
            "notes": "The tighter opener converted to a hire.",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["client_response_outcome"] == "hired"
    assert "converted to a hire" in update_response.json()["memory_text"]

    other_headers, _ = _register_user()
    forbidden_response = client.get(f"/history/feedback/{body['id']}", headers=other_headers)
    assert forbidden_response.status_code == 404


@pytest.mark.asyncio
async def test_feedback_rejects_duplicate_variant_feedback(db_session):
    headers, user_id = _register_user()
    variant = await _seed_generation_history(db_session, user_id)

    payload = {
        "generation_variant_id": str(variant.id),
        "rating": 4,
        "accepted_sections": ["Lead with the dashboard KPI issue"],
        "rejected_sections": [],
        "client_response_outcome": "replied",
    }
    first_response = client.post("/history/feedback", headers=headers, json=payload)
    assert first_response.status_code == 201

    duplicate_response = client.post("/history/feedback", headers=headers, json=payload)
    assert duplicate_response.status_code == 409
