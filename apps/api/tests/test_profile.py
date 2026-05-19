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


def test_projects_crud_flow(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    create_response = client.post(
        "/api/v1/profile/projects",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Lead Scoring AI",
            "description": "Built a scoring engine",
            "tech_stack": "FastAPI, PostgreSQL, LangChain",
            "impact": "+20% conversion",
            "project_url": "https://example.com/project",
        },
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    list_response = client.get("/api/v1/profile/projects", headers={"Authorization": f"Bearer {access_token}"})
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(f"/api/v1/profile/projects/{project_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert delete_response.status_code == 204


def test_professional_life_crud_flow(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    create_response = client.post(
        "/api/v1/profile/professional-life",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "company": "MGI",
            "role_title": "AI Engineer",
            "start_date": "2023-01-01",
            "summary": "Built AI automation pipelines",
        },
    )
    assert create_response.status_code == 201
    entry_id = create_response.json()["id"]

    list_response = client.get("/api/v1/profile/professional-life", headers={"Authorization": f"Bearer {access_token}"})
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(
        f"/api/v1/profile/professional-life/{entry_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert delete_response.status_code == 204


def test_custom_sections_crud_flow(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    create_response = client.post(
        "/api/v1/profile/custom-sections",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"section_name": "Client Communication Style", "content": "Direct and value-first"},
    )
    assert create_response.status_code == 201
    section_id = create_response.json()["id"]

    list_response = client.get("/api/v1/profile/custom-sections", headers={"Authorization": f"Bearer {access_token}"})
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(
        f"/api/v1/profile/custom-sections/{section_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert delete_response.status_code == 204

def test_project_patch_updates_existing_project(client: TestClient) -> None:
    access_token = _register_and_get_token(client)
    create = client.post(
        "/api/v1/profile/projects",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Initial Title"},
    )
    project_id = create.json()["id"]

    patch_response = client.patch(
        f"/api/v1/profile/projects/{project_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Updated Title", "impact": "Higher proposal win-rate"},
    )
    assert patch_response.status_code == 200
    data = patch_response.json()
    assert data["title"] == "Updated Title"
    assert data["impact"] == "Higher proposal win-rate"


def test_guidelines_and_samples_crud_and_patch_flow(client: TestClient) -> None:
    access_token = _register_and_get_token(client)

    guideline = client.post(
        "/api/v1/profile/guidelines",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Open strong", "content": "Mention relevance in first 2 lines", "priority": 1},
    )
    assert guideline.status_code == 201
    guideline_id = guideline.json()["id"]

    g_patch = client.patch(
        f"/api/v1/profile/guidelines/{guideline_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"priority": 2},
    )
    assert g_patch.status_code == 200
    assert g_patch.json()["priority"] == 2

    sample = client.post(
        "/api/v1/profile/samples",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "SaaS Job", "body": "Hi, I built similar SaaS products...", "tone": "professional"},
    )
    assert sample.status_code == 201
    sample_id = sample.json()["id"]

    s_patch = client.patch(
        f"/api/v1/profile/samples/{sample_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"tone": "friendly"},
    )
    assert s_patch.status_code == 200
    assert s_patch.json()["tone"] == "friendly"
