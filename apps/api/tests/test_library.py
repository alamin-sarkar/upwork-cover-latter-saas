import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _email() -> str:
    return f"library-{uuid.uuid4().hex[:10]}@acme.com"


def _auth_headers() -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={"email": _email(), "password": "Secret1234", "full_name": "Library Tester"},
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


GUIDELINE_CASES = [
    (
        {
            "title": "Lead with job context",
            "guideline_type": "rule",
            "description": "Core writing rule",
            "content": "Start with a concrete observation from the job post.",
            "sort_order": 1,
        },
        {"content": "Start with a job-specific observation, not a greeting."},
        "content",
        "Start with a job-specific observation, not a greeting.",
    ),
    (
        {
            "title": "Healthcare intro",
            "guideline_type": "intro",
            "description": "Reusable opener",
            "content": "Patient-facing AI work is a strong fit for my recent delivery history.",
            "sort_order": 2,
        },
        {"title": "Healthcare AI intro"},
        "title",
        "Healthcare AI intro",
    ),
    (
        {
            "title": "Clarifying CTA",
            "guideline_type": "cta",
            "description": "Reusable ending",
            "content": "What does success look like for the first 30 days of this project?",
            "sort_order": 3,
        },
        {"sort_order": 4},
        "sort_order",
        4,
    ),
    (
        {
            "title": "Confident tone",
            "guideline_type": "tone_preset",
            "description": "Default tone preset",
            "content": "Direct, proof-led, and concise. Avoid empty enthusiasm.",
            "sort_order": 4,
        },
        {"description": "Strong but measured tone preset"},
        "description",
        "Strong but measured tone preset",
    ),
]

SAMPLE_CASES = [
    (
        {
            "title": "Renewed React contract",
            "tag": "winning",
            "content": "I noticed you need someone who can own the React dashboard without hand-holding...",
            "notes": "Won a 6-month extension.",
            "outcome": "Client replied within 2 hours",
            "sort_order": 1,
        },
        {"tag": "anti-pattern", "notes": "Too generic in hindsight."},
        "tag",
        "anti-pattern",
    ),
    (
        {
            "title": "Generic opener example",
            "tag": "anti-pattern",
            "content": "Hello, I am writing to express my strong interest in your project...",
            "notes": "Too bland and interchangeable.",
            "outcome": "No reply",
            "sort_order": 2,
        },
        {"outcome": "Explicitly avoid this structure"},
        "outcome",
        "Explicitly avoid this structure",
    ),
]


class TestGuidelines:
    @pytest.mark.parametrize(
        ("create_payload", "update_payload", "updated_field", "updated_value"),
        GUIDELINE_CASES,
    )
    def test_guideline_crud(
        self,
        create_payload: dict,
        update_payload: dict,
        updated_field: str,
        updated_value,
    ):
        headers = _auth_headers()

        created = client.post("/library/guidelines", headers=headers, json=create_payload)
        assert created.status_code == 201
        body = created.json()
        guideline_id = body["id"]
        assert body["guideline_type"] == create_payload["guideline_type"]

        fetched = client.get(f"/library/guidelines/{guideline_id}", headers=headers)
        assert fetched.status_code == 200
        assert fetched.json()["id"] == guideline_id

        updated = client.patch(
            f"/library/guidelines/{guideline_id}",
            headers=headers,
            json=update_payload,
        )
        assert updated.status_code == 200
        assert updated.json()[updated_field] == updated_value

        deleted = client.delete(f"/library/guidelines/{guideline_id}", headers=headers)
        assert deleted.status_code == 204
        assert client.get(f"/library/guidelines/{guideline_id}", headers=headers).status_code == 404

    def test_guideline_listing_can_filter_by_type(self):
        headers = _auth_headers()

        for payload, *_ in GUIDELINE_CASES:
            response = client.post("/library/guidelines", headers=headers, json=payload)
            assert response.status_code == 201

        listing = client.get("/library/guidelines?guideline_type=tone_preset", headers=headers)
        assert listing.status_code == 200
        items = listing.json()
        assert len(items) == 1
        assert items[0]["guideline_type"] == "tone_preset"

    def test_invalid_guideline_type_returns_422(self):
        headers = _auth_headers()
        response = client.post(
            "/library/guidelines",
            headers=headers,
            json={
                "title": "Bad type",
                "guideline_type": "unknown",
                "content": "Should fail",
            },
        )
        assert response.status_code == 422


class TestSamples:
    @pytest.mark.parametrize(
        ("create_payload", "update_payload", "updated_field", "updated_value"),
        SAMPLE_CASES,
    )
    def test_sample_crud(
        self,
        create_payload: dict,
        update_payload: dict,
        updated_field: str,
        updated_value,
    ):
        headers = _auth_headers()

        created = client.post("/library/samples", headers=headers, json=create_payload)
        assert created.status_code == 201
        body = created.json()
        sample_id = body["id"]
        assert body["tag"] == create_payload["tag"]

        fetched = client.get(f"/library/samples/{sample_id}", headers=headers)
        assert fetched.status_code == 200
        assert fetched.json()["id"] == sample_id

        updated = client.patch(
            f"/library/samples/{sample_id}",
            headers=headers,
            json=update_payload,
        )
        assert updated.status_code == 200
        assert updated.json()[updated_field] == updated_value

        deleted = client.delete(f"/library/samples/{sample_id}", headers=headers)
        assert deleted.status_code == 204
        assert client.get(f"/library/samples/{sample_id}", headers=headers).status_code == 404

    def test_sample_listing_can_filter_by_tag(self):
        headers = _auth_headers()

        for payload, *_ in SAMPLE_CASES:
            response = client.post("/library/samples", headers=headers, json=payload)
            assert response.status_code == 201

        listing = client.get("/library/samples?tag=winning", headers=headers)
        assert listing.status_code == 200
        items = listing.json()
        assert len(items) == 1
        assert items[0]["tag"] == "winning"

    def test_invalid_sample_tag_returns_422(self):
        headers = _auth_headers()
        response = client.post(
            "/library/samples",
            headers=headers,
            json={
                "title": "Bad tag",
                "tag": "neutral",
                "content": "Should fail",
            },
        )
        assert response.status_code == 422


class TestLibraryOwnershipIsolation:
    def test_guidelines_are_scoped_to_owner(self):
        owner_headers = _auth_headers()
        other_headers = _auth_headers()

        created = client.post(
            "/library/guidelines",
            headers=owner_headers,
            json=GUIDELINE_CASES[0][0],
        )
        assert created.status_code == 201
        guideline_id = created.json()["id"]

        assert (
            client.get(f"/library/guidelines/{guideline_id}", headers=other_headers).status_code
            == 404
        )
        assert (
            client.patch(
                f"/library/guidelines/{guideline_id}",
                headers=other_headers,
                json={"content": "Hijack attempt"},
            ).status_code
            == 404
        )
        assert (
            client.delete(f"/library/guidelines/{guideline_id}", headers=other_headers).status_code
            == 404
        )

    def test_samples_are_scoped_to_owner(self):
        owner_headers = _auth_headers()
        other_headers = _auth_headers()

        created = client.post(
            "/library/samples",
            headers=owner_headers,
            json=SAMPLE_CASES[0][0],
        )
        assert created.status_code == 201
        sample_id = created.json()["id"]

        assert client.get(f"/library/samples/{sample_id}", headers=other_headers).status_code == 404
        assert (
            client.patch(
                f"/library/samples/{sample_id}",
                headers=other_headers,
                json={"notes": "Hijack attempt"},
            ).status_code
            == 404
        )
        assert client.delete(f"/library/samples/{sample_id}", headers=other_headers).status_code == 404
