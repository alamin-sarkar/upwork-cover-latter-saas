import json
import uuid

import pytest
from ai_workflows.generation.schemas import CoverLetterReviewResult, DraftedCoverLetter
from ai_workflows.job_analysis import JobAnalysis
from fastapi.testclient import TestClient

from app.api.routes import mcp as mcp_route
from app.main import app
from app.models.job_analysis import JobAnalysisSnapshot
from app.models.library import CoverLetterGuideline, CoverLetterSample
from app.models.profile import Profile, ProfilePreferences, ProfileProject, ProfileSkill
from app.services.generation import CoverLetterGenerationService

client = TestClient(app)


def _email() -> str:
    return f"mcp-{uuid.uuid4().hex[:10]}@acme.com"


def _register_user() -> tuple[dict[str, str], uuid.UUID]:
    response = client.post(
        "/auth/register",
        json={
            "email": _email(),
            "password": "Secret1234",
            "full_name": "MCP Tester",
        },
    )
    assert response.status_code == 201
    body = response.json()
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    me_response = client.get("/auth/me", headers=headers)
    assert me_response.status_code == 200
    return headers, uuid.UUID(me_response.json()["id"])


ANALYSIS = JobAnalysis(
    title="Senior React Dashboard Engineer",
    scope="Own a reporting dashboard rebuild for a B2B SaaS product.",
    deliverables=[
        "Deliver a new analytics dashboard",
        "Integrate reporting APIs",
    ],
    required_skills=["React", "TypeScript", "API integration"],
    budget_clues=["Senior ownership expected"],
    urgency="high",
    tone="demanding",
    risk_flags=["Tight deadline"],
    fit_score=88,
)


class FakeJobAnalysisService:
    async def analyze_job_post(self, *, user_id, raw_job_text, session):
        snapshot = JobAnalysisSnapshot(
            user_id=user_id,
            raw_job_text=raw_job_text,
            title=ANALYSIS.title,
            scope=ANALYSIS.scope,
            deliverables=ANALYSIS.deliverables,
            required_skills=ANALYSIS.required_skills,
            budget_clues=ANALYSIS.budget_clues,
            urgency=ANALYSIS.urgency.value,
            tone=ANALYSIS.tone.value,
            risk_flags=ANALYSIS.risk_flags,
            fit_score=ANALYSIS.fit_score,
            analysis_payload=ANALYSIS.model_dump(mode="json"),
            provider="anthropic",
            model_name="claude-test",
            prompt_version="test-analysis",
        )
        session.add(snapshot)
        await session.commit()
        await session.refresh(snapshot)
        return snapshot


class FakeStructuredModel:
    def __init__(self, schema, queue):
        self.schema = schema
        self.queue = queue

    async def ainvoke(self, messages):
        payload = self.queue.pop(0)
        return self.schema.model_validate(payload)


class FakeStructuredFactory:
    def __init__(self, *, draft_payloads, review_payloads):
        self._draft_payloads = list(draft_payloads)
        self._review_payloads = list(review_payloads)

    def __call__(self, schema):
        if schema is DraftedCoverLetter:
            return FakeStructuredModel(schema, self._draft_payloads)
        if schema is CoverLetterReviewResult:
            return FakeStructuredModel(schema, self._review_payloads)
        raise AssertionError(f"Unexpected schema requested: {schema}")


async def _seed_profile_and_library(db_session, user_id: uuid.UUID):
    profile = Profile(
        user_id=user_id,
        professional_title="Senior React Engineer",
        about="I build analytics products for B2B SaaS teams.",
        availability_note="Can start this week.",
    )
    profile.skills.append(
        ProfileSkill(
            name="React",
            level="expert",
            proof="Shipped multiple enterprise dashboards.",
            sort_order=0,
        )
    )
    profile.projects.append(
        ProfileProject(
            title="Revenue Ops Dashboard",
            description="Built a live KPI dashboard for account executives.",
            outcome="Cut reporting delays from days to minutes.",
            sort_order=0,
        )
    )
    profile.preferences = ProfilePreferences(
        default_tone="direct",
        voice_note="Lead with proof, not hype.",
        cta_style="ask one sharp question",
    )
    db_session.add(profile)
    db_session.add(
        CoverLetterGuideline(
            user_id=user_id,
            title="Lead with context",
            guideline_type="rule",
            content="Open with an observation from the job post.",
            sort_order=0,
        )
    )
    db_session.add(
        CoverLetterSample(
            user_id=user_id,
            title="Winning dashboard sample",
            tag="winning",
            content="I rebuilt a dashboard that reduced lag and increased trust in the data.",
            notes="Strong proof-led opener.",
            sort_order=0,
        )
    )
    await db_session.commit()


def _mcp_request(token: str, method: str, params: dict | None = None, request_id: int = 1):
    return client.post(
        "/mcp",
        headers={"Authorization": f"Bearer {token}"},
        json={"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}},
    )


def test_mcp_token_crud_flow():
    headers, _ = _register_user()

    create_response = client.post("/mcp/tokens", headers=headers, json={"label": "Claude Desktop"})
    assert create_response.status_code == 201
    token_body = create_response.json()
    assert token_body["token"].startswith("mcp_")
    assert token_body["token_prefix"] == token_body["token"][:24]

    list_response = client.get("/mcp/tokens", headers=headers)
    assert list_response.status_code == 200
    assert [item["label"] for item in list_response.json()] == ["Claude Desktop"]

    revoke_response = client.delete(f"/mcp/tokens/{token_body['id']}", headers=headers)
    assert revoke_response.status_code == 204

    rpc_response = _mcp_request(token_body["token"], "resources/list")
    assert rpc_response.status_code == 401
    assert rpc_response.json()["detail"] == "Invalid MCP token"


@pytest.mark.asyncio
async def test_mcp_resources_and_generate_tool_smoke(db_session):
    headers, user_id = _register_user()
    await _seed_profile_and_library(db_session, user_id)

    token_response = client.post("/mcp/tokens", headers=headers, json={"label": "OpenAI MCP"})
    assert token_response.status_code == 201
    mcp_token = token_response.json()["token"]

    factory = FakeStructuredFactory(
        draft_payloads=[
            {
                "structure": "concise",
                "headline": "React dashboard delivery",
                "cover_letter": "I've shipped React reporting systems for B2B SaaS teams and can own this rebuild end to end.",
                "rationale": "Fast, direct variant for a high-urgency post.",
                "match_notes": ["Directly matches React dashboard scope"],
            }
        ],
        review_payloads=[
            {
                "structure": "concise",
                "final_headline": "React dashboard delivery",
                "final_cover_letter": "I've shipped React reporting systems for B2B SaaS teams and can own this rebuild end to end. I'd start by tightening data flows and the slowest UI paths.",
                "final_rationale": "Keeps the concise structure while adding a specific first-step signal.",
                "final_match_notes": ["React + dashboard fit"],
                "self_check_notes": ["Added a concrete first-step statement"],
            }
        ],
    )

    original_factory = mcp_route.get_mcp_generation_service
    mcp_route.get_mcp_generation_service = lambda: CoverLetterGenerationService(
        draft_model_factory=factory,
        review_model_factory=factory,
        job_analysis_service=FakeJobAnalysisService(),
    )

    try:
        init_response = _mcp_request(
            mcp_token,
            "initialize",
            {"protocolVersion": "2024-11-05", "clientInfo": {"name": "smoke-test", "version": "1.0"}},
        )
        assert init_response.status_code == 200
        assert init_response.json()["result"]["serverInfo"]["name"] == "upwork-cover-letter-mcp"

        resources_response = _mcp_request(mcp_token, "resources/list")
        resources = resources_response.json()["result"]["resources"]
        assert [item["uri"] for item in resources] == [
            "pitchcraft://profile",
            "pitchcraft://guidelines",
            "pitchcraft://samples",
        ]

        profile_response = _mcp_request(
            mcp_token,
            "resources/read",
            {"uri": "pitchcraft://profile"},
        )
        profile_payload = json.loads(profile_response.json()["result"]["contents"][0]["text"])
        assert profile_payload["profile"]["professional_title"] == "Senior React Engineer"

        guidelines_response = _mcp_request(
            mcp_token,
            "resources/read",
            {"uri": "pitchcraft://guidelines"},
        )
        guidelines_payload = json.loads(guidelines_response.json()["result"]["contents"][0]["text"])
        assert guidelines_payload["guidelines"][0]["title"] == "Lead with context"

        tools_response = _mcp_request(mcp_token, "tools/list")
        tools = tools_response.json()["result"]["tools"]
        assert tools[0]["name"] == "generate_cover_letter"

        call_response = _mcp_request(
            mcp_token,
            "tools/call",
            {
                "name": "generate_cover_letter",
                "arguments": {
                    "raw_job_text": (
                        "We need a senior React engineer to rebuild our analytics dashboard. "
                        "You should be comfortable with TypeScript and API integrations."
                    ),
                    "structures": ["concise"],
                },
            },
        )
    finally:
        mcp_route.get_mcp_generation_service = original_factory

    assert call_response.status_code == 200
    result = call_response.json()["result"]
    assert result["isError"] is False
    assert result["structuredContent"]["analysis"]["title"] == ANALYSIS.title
    assert result["structuredContent"]["variants"][0]["structure"] == "concise"
