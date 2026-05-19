from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

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


def test_register_returns_user_and_tokens(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "alamin@example.com"
    assert data["user"]["plan"] == "free"
    assert data["tokens"]["access_token"]
    assert data["tokens"]["refresh_token"]
    assert data["tokens"]["token_type"] == "bearer"


def test_register_rejects_duplicate_email(client: TestClient) -> None:
    payload = {
        "full_name": "Alamin Sarkar",
        "email": "alamin@example.com",
        "password": "strongpass123",
    }

    first_response = client.post("/api/v1/auth/register", json=payload)
    second_response = client.post("/api/v1/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"


def test_login_returns_tokens_for_valid_credentials(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "alamin@example.com", "password": "strongpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_login_rejects_invalid_password(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "alamin@example.com", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_me_returns_current_user_from_access_token(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    access_token = register_response.json()["tokens"]["access_token"]
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alamin@example.com"
    assert data["full_name"] == "Alamin Sarkar"


def test_refresh_returns_new_token_pair(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    refresh_token = register_response.json()["tokens"]["refresh_token"]
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_refresh_rejects_access_token(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Alamin Sarkar",
            "email": "alamin@example.com",
            "password": "strongpass123",
        },
    )

    access_token = register_response.json()["tokens"]["access_token"]
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": access_token},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"
