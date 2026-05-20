import uuid

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.routes import admin as admin_route
from app.core.config import Settings, get_settings
from app.core.rate_limits import _memory_storage
from app.main import app
import app.main as main_module

client = TestClient(app)


def _email() -> str:
    return f"hardening-{uuid.uuid4().hex[:10]}@acme.com"


def _auth_headers() -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={"email": _email(), "password": "Secret1234", "full_name": "Hardening Tester"},
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health_sets_request_id_header():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_readiness_reports_dependency_state(monkeypatch):
    async def fake_db():
        return {"ok": True}

    async def fake_redis():
        return {"ok": True}

    monkeypatch.setattr(main_module, "check_database", fake_db)
    monkeypatch.setattr(main_module, "check_redis", fake_redis)

    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_admin_diagnostics_returns_request_context(monkeypatch):
    settings = get_settings()
    original_token = settings.admin_diagnostics_token
    settings.admin_diagnostics_token = "diagnostics-secret-token"

    async def fake_db():
        return {"ok": True}

    async def fake_redis():
        return {"ok": True}

    async def fake_celery():
        return {"ok": True, "workers": {"worker@local": {"ok": "pong"}}}

    monkeypatch.setattr(admin_route, "check_database", fake_db)
    monkeypatch.setattr(admin_route, "check_redis", fake_redis)
    monkeypatch.setattr(admin_route, "check_celery_workers", fake_celery)

    response = client.get(
        "/admin/diagnostics",
        headers={"X-Admin-Token": settings.admin_diagnostics_token},
    )

    settings.admin_diagnostics_token = original_token

    assert response.status_code == 200
    body = response.json()
    assert body["request_id"]
    assert body["dependencies"]["celery"]["ok"] is True


def test_settings_reject_insecure_production_config():
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            docs_enabled=True,
            jwt_secret="change-me-in-production",
            admin_diagnostics_token="short",
        )


def test_generation_rate_limit_enforced():
    settings = get_settings()
    original_limits = settings.generation_daily_limits.copy()
    settings.generation_daily_limits = {"free": 1, "pro": 1, "team": 1}
    _memory_storage._store.clear()

    headers = _auth_headers()

    first = client.post(
        "/generate",
        headers=headers,
        json={"analysis_snapshot_id": str(uuid.uuid4())},
    )
    assert first.status_code in {404, 503}

    second = client.post(
        "/generate",
        headers=headers,
        json={"analysis_snapshot_id": str(uuid.uuid4())},
    )
    settings.generation_daily_limits = original_limits

    assert second.status_code == 429
