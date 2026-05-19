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
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
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
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )
    assert response.status_code == 201
    return response.json()["tokens"]["access_token"]


def test_get_profile_auto_creates_profile(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    response = client.get("/api/v1/profile", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["headline"] is None
    assert data["professional_summary"] is None


def test_update_profile_persists_headline_and_summary(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    response = client.put(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"headline": "AI Engineer", "professional_summary": "I build reliable AI systems."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["headline"] == "AI Engineer"
    assert data["professional_summary"] == "I build reliable AI systems."


def test_add_and_list_skills(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    create_response = client.post(
        "/api/v1/profile/skills",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "FastAPI", "proficiency": "advanced", "years_experience": 3},
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/v1/profile/skills", headers={"Authorization": f"Bearer {access_token}"})
    assert list_response.status_code == 200
    skills = list_response.json()
    assert len(skills) == 1
    assert skills[0]["name"] == "FastAPI"


def test_duplicate_skill_is_rejected(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    payload = {"name": "LangGraph", "proficiency": "intermediate", "years_experience": 2}
    first = client.post("/api/v1/profile/skills", headers={"Authorization": f"Bearer {access_token}"}, json=payload)
    second = client.post("/api/v1/profile/skills", headers={"Authorization": f"Bearer {access_token}"}, json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "Skill already exists"
