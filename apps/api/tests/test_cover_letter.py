from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base
from app.core.deps import get_db
from app.main import app
from app.services import cover_letter_graph as graph_service

SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _register_and_get_token(client: TestClient) -> str:
    response = client.post("/api/v1/auth/register", json={"full_name": "Alamin Sarkar", "email": "alamin@example.com", "password": "strongpass123"})
    assert response.status_code == 201
    return response.json()["tokens"]["access_token"]


def test_cover_letter_engine_scaffold_flow(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    job = client.post(
        "/api/v1/cover-letter/job-posts",
        headers=headers,
        json={
            "title": "Need AI SaaS developer for Upwork proposal automation",
            "raw_text": "We need a FastAPI + Next.js expert to build an AI engine for cover letter generation with reusable templates and history.",
            "source": "upwork",
        },
    )
    assert job.status_code == 201
    job_id = job.json()["id"]

    generated = client.post("/api/v1/cover-letter/generate", headers=headers, json={"job_post_id": job_id})
    assert generated.status_code == 200
    variants = generated.json()
    assert len(variants) == 3
    assert variants[0]["structure"] in {"direct-value", "problem-solution", "story-proof"}

    history = client.get("/api/v1/cover-letter/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) >= 3

def test_feedback_memory_loop_applies_signal(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    job = client.post(
        "/api/v1/cover-letter/job-posts",
        headers=headers,
        json={
            "title": "Need FastAPI expert",
            "raw_text": "Need someone who can build robust APIs quickly with clear communication and concrete milestones.",
            "source": "upwork",
        },
    )
    assert job.status_code == 201
    job_id = job.json()["id"]

    first_generation = client.post("/api/v1/cover-letter/generate", headers=headers, json={"job_post_id": job_id})
    assert first_generation.status_code == 200
    generation_id = first_generation.json()[0]["id"]

    feedback = client.post(
        "/api/v1/cover-letter/feedback",
        headers=headers,
        json={"generation_id": generation_id, "rating": 2, "feedback_text": "Too generic. Make it concise and specific."},
    )
    assert feedback.status_code == 201

    memory_signal = client.get("/api/v1/cover-letter/memory-signal", headers=headers)
    assert memory_signal.status_code == 200
    signal = memory_signal.json()
    assert signal["avg_rating"] == 2.0
    assert signal["preferred_tone"] == "concise"
    assert "shorter-letters" in signal["do_more"]
    assert "generic-lines" in signal["avoid"]

    second_generation = client.post("/api/v1/cover-letter/generate", headers=headers, json={"job_post_id": job_id})
    assert second_generation.status_code == 200
    assert "make letters more specific and concise" in second_generation.json()[0]["analysis_summary"].lower()


def test_langgraph_orchestration_path_in_generation(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    job = client.post(
        "/api/v1/cover-letter/job-posts",
        headers=headers,
        json={
            "title": "Build LangGraph workflow",
            "raw_text": "Need a developer to orchestrate multiple cover letter generation strategies with structured reasoning.",
            "source": "upwork",
        },
    )
    assert job.status_code == 201

    generated = client.post(
        "/api/v1/cover-letter/generate",
        headers=headers,
        json={"job_post_id": job.json()["id"]},
    )
    assert generated.status_code == 200
    variants = generated.json()
    assert len(variants) == 3
    assert all("Analyze:" in v["analysis_summary"] for v in variants)

def test_structure_wise_output_parser_behavior(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    job = client.post(
        "/api/v1/cover-letter/job-posts",
        headers=headers,
        json={
            "title": "Need proposal automation engineer",
            "raw_text": "Need FastAPI + LangGraph engineer to produce multiple tailored proposal styles with memory-aware outputs.",
            "source": "upwork",
        },
    )
    assert job.status_code == 201

    generated = client.post(
        "/api/v1/cover-letter/generate",
        headers=headers,
        json={"job_post_id": job.json()["id"]},
    )
    assert generated.status_code == 200
    variants = generated.json()
    structures = {v["structure"] for v in variants}
    assert structures == {"direct-value", "problem-solution", "story-proof"}
    assert all(v["draft_text"] for v in variants)
    assert all(v["analysis_summary"].startswith("Analyze:") for v in variants)

def test_provider_fallback_error_safe_contract(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    job = client.post(
        "/api/v1/cover-letter/job-posts",
        headers=headers,
        json={
            "title": "Need API fallback wiring",
            "raw_text": "Need robust provider fallback chain with timeout and retry.",
            "source": "upwork",
        },
    )
    assert job.status_code == 201

    generated = client.post(
        "/api/v1/cover-letter/generate",
        headers=headers,
        json={"job_post_id": job.json()["id"]},
    )
    assert generated.status_code == 200
    data = generated.json()
    assert len(data) == 3
    assert all(item["analysis_summary"] for item in data)
    assert all(item["draft_text"] for item in data)


def test_provider_health_check_and_model_mapping() -> None:
    specs = graph_service._provider_candidates()
    assert specs[0].name in {"openrouter", "groq", "gemini", "mock"}
    non_mock = [s for s in specs if s.name != "mock"]
    assert all(s.model for s in non_mock)

    ok, reason = graph_service._provider_health_check(non_mock[0])
    if ok:
        assert reason is None
    else:
        assert "API_KEY" in reason or "invalid" in reason


def test_strict_schema_parser_deterministic_recovery() -> None:
    state = {
        "job_title": "Need FastAPI dev",
        "raw_text": "x",
        "headline": "Engineer",
        "guideline_text": "Be concise",
        "tone_hint": "professional",
        "preference_note": "",
        "structure": "direct-value",
        "analysis_summary": "",
        "draft_text": "",
        "prompt_text": "",
        "llm_raw_output": '{"analysis_summary": 42, "draft_text": null}',
        "telemetry": {},
    }
    out = graph_service._parse_output(state)
    assert out["analysis_summary"].startswith("Analyze:")
    assert out["draft_text"]
    assert out["telemetry"].get("parser_recovery") is True
