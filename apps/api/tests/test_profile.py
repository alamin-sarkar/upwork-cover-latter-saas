import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _email() -> str:
    return f"profile-{uuid.uuid4().hex[:10]}@acme.com"


def _auth_headers() -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={"email": _email(), "password": "Secret1234", "full_name": "Profile Tester"},
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_profile(headers: dict[str, str]) -> dict:
    response = client.post(
        "/profile",
        headers=headers,
        json={
            "professional_title": "AI Engineer",
            "location": "Dhaka, Bangladesh",
            "hourly_rate_usd": 65,
            "about": "Builds AI SaaS products with strong delivery discipline.",
            "availability_note": "Available for long-term contracts.",
        },
    )
    assert response.status_code == 201
    return response.json()


SECTION_CASES = [
    (
        "skills",
        {
            "name": "React",
            "level": "Expert",
            "years_of_experience": 5,
            "proof": "Shipped multiple production dashboards.",
            "sort_order": 1,
        },
        {"level": "Advanced", "sort_order": 2},
        "level",
        "Advanced",
    ),
    (
        "projects",
        {
            "title": "DocuChat AI",
            "role": "Lead Engineer",
            "tagline": "RAG SaaS for support teams",
            "description": "Built ingestion, retrieval, and evaluation flows.",
            "outcome": "12K MAU",
            "link": "https://example.com/docuchat",
            "stack": ["Next.js", "Python", "PostgreSQL"],
            "evidence_points": ["Reduced latency by 60%"],
            "sort_order": 1,
        },
        {"outcome": "15K MAU", "sort_order": 3},
        "outcome",
        "15K MAU",
    ),
    (
        "experiences",
        {
            "company": "Lumen Health",
            "role": "Senior AI Engineer",
            "start_date": "2024-01-01",
            "end_date": "2025-01-01",
            "is_current": False,
            "summary": "Owned patient support automation.",
            "highlights": ["Cut hallucinations to 2.1%"],
            "sort_order": 1,
        },
        {"is_current": True, "summary": "Owns patient support automation."},
        "is_current",
        True,
    ),
    (
        "niches",
        {
            "name": "Legal tech",
            "summary": "Strong fit for compliance-heavy domains.",
            "proof": "Delivered tools for audit and contract review.",
            "sort_order": 1,
        },
        {"summary": "Strong fit for regulated software."},
        "summary",
        "Strong fit for regulated software.",
    ),
    (
        "custom-sections",
        {
            "title": "Certifications",
            "section_type": "certifications",
            "content": "AWS Solutions Architect Associate (2024)",
            "sort_order": 1,
        },
        {"content": "AWS Solutions Architect Associate (2025)"},
        "content",
        "AWS Solutions Architect Associate (2025)",
    ),
]


class TestProfileRoot:
    def test_profile_root_crud(self):
        headers = _auth_headers()

        created = _create_profile(headers)
        assert created["professional_title"] == "AI Engineer"

        fetched = client.get("/profile", headers=headers)
        assert fetched.status_code == 200
        body = fetched.json()
        assert body["location"] == "Dhaka, Bangladesh"
        assert body["skills"] == []
        assert body["preferences"] is None

        updated = client.patch(
            "/profile",
            headers=headers,
            json={"professional_title": "Principal AI Engineer", "hourly_rate_usd": 80},
        )
        assert updated.status_code == 200
        assert updated.json()["professional_title"] == "Principal AI Engineer"
        assert updated.json()["hourly_rate_usd"] == 80.0

        duplicate = client.post("/profile", headers=headers, json={})
        assert duplicate.status_code == 409

        deleted = client.delete("/profile", headers=headers)
        assert deleted.status_code == 204
        assert client.get("/profile", headers=headers).status_code == 404

    def test_profile_requires_auth(self):
        response = client.get("/profile")
        assert response.status_code == 401


class TestProfileSections:
    @pytest.mark.parametrize(
        ("section", "create_payload", "update_payload", "updated_field", "updated_value"),
        SECTION_CASES,
    )
    def test_section_crud(
        self,
        section: str,
        create_payload: dict,
        update_payload: dict,
        updated_field: str,
        updated_value,
    ):
        headers = _auth_headers()

        created = client.post(f"/profile/{section}", headers=headers, json=create_payload)
        assert created.status_code == 201
        item = created.json()
        item_id = item["id"]
        assert item["sort_order"] == create_payload.get("sort_order", 0)

        listing = client.get(f"/profile/{section}", headers=headers)
        assert listing.status_code == 200
        assert len(listing.json()) == 1

        fetched = client.get(f"/profile/{section}/{item_id}", headers=headers)
        assert fetched.status_code == 200
        assert fetched.json()["id"] == item_id

        updated = client.patch(
            f"/profile/{section}/{item_id}",
            headers=headers,
            json=update_payload,
        )
        assert updated.status_code == 200
        assert updated.json()[updated_field] == updated_value

        deleted = client.delete(f"/profile/{section}/{item_id}", headers=headers)
        assert deleted.status_code == 204
        assert client.get(f"/profile/{section}", headers=headers).json() == []

    def test_invalid_skill_payload_returns_422(self):
        headers = _auth_headers()
        response = client.post(
            "/profile/skills",
            headers=headers,
            json={"name": "", "years_of_experience": -1},
        )
        assert response.status_code == 422


class TestProfilePreferences:
    def test_preferences_crud(self):
        headers = _auth_headers()

        created = client.post(
            "/profile/preferences",
            headers=headers,
            json={
                "default_tone": "confident",
                "voice_note": "Lead with proof, not promises.",
                "avoid_phrases": ["I am writing to express my interest"],
                "preferred_length": "short",
                "cta_style": "question",
                "signature": "Best,\nRakib",
                "extra_instructions": "Mirror the client's vocabulary.",
            },
        )
        assert created.status_code == 201
        assert created.json()["default_tone"] == "confident"

        duplicate = client.post("/profile/preferences", headers=headers, json={})
        assert duplicate.status_code == 409

        fetched = client.get("/profile/preferences", headers=headers)
        assert fetched.status_code == 200
        assert fetched.json()["preferred_length"] == "short"

        updated = client.patch(
            "/profile/preferences",
            headers=headers,
            json={"preferred_length": "medium", "avoid_phrases": ["generic praise"]},
        )
        assert updated.status_code == 200
        assert updated.json()["preferred_length"] == "medium"
        assert updated.json()["avoid_phrases"] == ["generic praise"]

        deleted = client.delete("/profile/preferences", headers=headers)
        assert deleted.status_code == 204
        assert client.get("/profile/preferences", headers=headers).status_code == 404


class TestOwnershipIsolation:
    @pytest.mark.parametrize("section,create_payload,_,__,___", SECTION_CASES)
    def test_section_items_are_scoped_to_owner(
        self,
        section: str,
        create_payload: dict,
        _,
        __,
        ___,
    ):
        owner_headers = _auth_headers()
        other_headers = _auth_headers()

        created = client.post(f"/profile/{section}", headers=owner_headers, json=create_payload)
        assert created.status_code == 201
        item_id = created.json()["id"]

        assert client.get(f"/profile/{section}/{item_id}", headers=other_headers).status_code == 404
        assert (
            client.patch(
                f"/profile/{section}/{item_id}",
                headers=other_headers,
                json=create_payload,
            ).status_code
            == 404
        )
        assert client.delete(f"/profile/{section}/{item_id}", headers=other_headers).status_code == 404


class TestCascadeDelete:
    def test_deleting_profile_removes_all_child_sections(self):
        headers = _auth_headers()
        _create_profile(headers)

        client.post("/profile/skills", headers=headers, json=SECTION_CASES[0][1])
        client.post("/profile/projects", headers=headers, json=SECTION_CASES[1][1])
        client.post("/profile/experiences", headers=headers, json=SECTION_CASES[2][1])
        client.post("/profile/niches", headers=headers, json=SECTION_CASES[3][1])
        client.post("/profile/custom-sections", headers=headers, json=SECTION_CASES[4][1])
        client.post(
            "/profile/preferences",
            headers=headers,
            json={"default_tone": "direct", "avoid_phrases": ["generic opener"]},
        )

        deleted = client.delete("/profile", headers=headers)
        assert deleted.status_code == 204

        assert client.get("/profile", headers=headers).status_code == 404
        assert client.get("/profile/preferences", headers=headers).status_code == 404
        assert client.get("/profile/skills", headers=headers).json() == []
        assert client.get("/profile/projects", headers=headers).json() == []
        assert client.get("/profile/experiences", headers=headers).json() == []
        assert client.get("/profile/niches", headers=headers).json() == []
        assert client.get("/profile/custom-sections", headers=headers).json() == []
