from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base
from app.core.deps import get_db
from app.main import app

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
