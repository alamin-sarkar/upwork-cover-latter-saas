"""
Auth endpoint integration tests.

Each test generates a UUID-based email so tests are fully independent
without requiring DB rollback or cleanup fixtures.
"""
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _email() -> str:
    # Use .com domain — email-validator rejects reserved TLDs like .test, .local, .invalid.
    return f"test-{uuid.uuid4().hex[:10]}@acme.com"


def _register(email: str | None = None, password: str = "Secret1234") -> dict:
    if email is None:
        email = _email()
    r = client.post("/auth/register", json={"email": email, "password": password})
    return r


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------


class TestRegister:
    def test_register_happy_path_returns_201_and_tokens(self):
        r = _register()
        assert r.status_code == 201
        body = r.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"

    def test_register_with_full_name(self):
        r = client.post(
            "/auth/register",
            json={"email": _email(), "password": "Secret1234", "full_name": "Jane Doe"},
        )
        assert r.status_code == 201

    def test_register_duplicate_email_returns_409(self):
        email = _email()
        _register(email)
        r = _register(email)
        assert r.status_code == 409

    def test_register_short_password_returns_422(self):
        r = _register(password="short")
        assert r.status_code == 422

    def test_register_invalid_email_returns_422(self):
        r = client.post(
            "/auth/register", json={"email": "not-an-email", "password": "Secret1234"}
        )
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


class TestLogin:
    def test_login_happy_path_returns_200_and_tokens(self):
        email = _email()
        _register(email)
        r = client.post("/auth/login", json={"email": email, "password": "Secret1234"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password_returns_401(self):
        email = _email()
        _register(email)
        r = client.post("/auth/login", json={"email": email, "password": "WrongPass!"})
        assert r.status_code == 401

    def test_login_unknown_email_returns_401(self):
        r = client.post(
            "/auth/login", json={"email": "nobody@acme.com", "password": "any"}
        )
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


class TestRefresh:
    def test_refresh_returns_new_tokens(self):
        reg = _register().json()
        r = client.post("/auth/refresh", json={"refresh_token": reg["refresh_token"]})
        assert r.status_code == 200
        body = r.json()
        assert "access_token" in body
        assert "refresh_token" in body

    def test_refresh_with_access_token_returns_401(self):
        reg = _register().json()
        r = client.post("/auth/refresh", json={"refresh_token": reg["access_token"]})
        assert r.status_code == 401

    def test_refresh_with_garbage_returns_401(self):
        r = client.post("/auth/refresh", json={"refresh_token": "not.a.jwt.token"})
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Me
# ---------------------------------------------------------------------------


class TestMe:
    def test_me_returns_authenticated_user(self):
        email = _email()
        reg = _register(email).json()
        r = client.get("/auth/me", headers={"Authorization": f"Bearer {reg['access_token']}"})
        assert r.status_code == 200
        body = r.json()
        assert body["email"] == email
        assert body["plan"] == "free"
        assert body["is_active"] is True
        assert "id" in body

    def test_me_no_token_returns_401(self):
        # FastAPI 0.115+ HTTPBearer returns 401 when the Authorization header is absent.
        r = client.get("/auth/me")
        assert r.status_code == 401

    def test_me_invalid_token_returns_401(self):
        r = client.get("/auth/me", headers={"Authorization": "Bearer bad.token.here"})
        assert r.status_code == 401

    def test_me_with_refresh_token_returns_401(self):
        reg = _register().json()
        r = client.get(
            "/auth/me", headers={"Authorization": f"Bearer {reg['refresh_token']}"}
        )
        assert r.status_code == 401
