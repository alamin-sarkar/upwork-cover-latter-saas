import uuid

import pytest
from ai_workflows.generation.schemas import CoverLetterReviewResult, DraftedCoverLetter
from ai_workflows.job_analysis import JobAnalysis
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.routes import generation as generation_route
from app.main import app
from app.models.feedback import CoverLetterFeedback
from app.models.generation import CoverLetterGenerationRun, CoverLetterGenerationVariant
from app.models.job_analysis import JobAnalysisSnapshot
from app.models.library import CoverLetterGuideline, CoverLetterSample
from app.models.profile import Profile, ProfilePreferences, ProfileProject, ProfileSkill
from app.services.feedback_memory import build_feedback_memory_text, embed_text
from app.services.generation import CoverLetterGenerationService

client = TestClient(app)


def _email() -> str:
    return f"generation-{uuid.uuid4().hex[:10]}@acme.com"


def _register_user() -> tuple[dict[str, str], uuid.UUID]:
    response = client.post(
        "/auth/register",
        json={
            "email": _email(),
            "password": "Secret1234",
            "full_name": "Generation Tester",
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
        "Improve performance bottlenecks",
    ],
    required_skills=["React", "TypeScript", "API integration"],
    budget_clues=["Senior ownership expected", "Fast delivery timeline"],
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
    def __init__(self, schema, queue, calls):
        self.schema = schema
        self.queue = queue
        self.calls = calls

    async def ainvoke(self, messages):
        self.calls.append(
            {
                "schema": self.schema.__name__,
                "messages": [getattr(message, "content", str(message)) for message in messages],
            }
        )
        payload = self.queue.pop(0)
        return self.schema.model_validate(payload)


class FakeStructuredFactory:
    def __init__(self, *, draft_payloads, review_payloads):
        self.calls = []
        self._draft_payloads = list(draft_payloads)
        self._review_payloads = list(review_payloads)

    def __call__(self, schema):
        if schema is DraftedCoverLetter:
            return FakeStructuredModel(schema, self._draft_payloads, self.calls)
        if schema is CoverLetterReviewResult:
            return FakeStructuredModel(schema, self._review_payloads, self.calls)
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


@pytest.mark.asyncio
async def test_generate_returns_multiple_variants_and_persists_run(db_session):
    headers, user_id = _register_user()
    await _seed_profile_and_library(db_session, user_id)

    factory = FakeStructuredFactory(
        draft_payloads=[
            {
                "structure": "concise",
                "headline": "React dashboard delivery",
                "cover_letter": "I’ve shipped React reporting systems for B2B SaaS teams and can own this rebuild end to end.",
                "rationale": "Fast, direct variant for a high-urgency post.",
                "match_notes": ["Directly matches React dashboard scope", "Uses SaaS analytics proof"],
            },
            {
                "structure": "problem-solution",
                "headline": "Fix the reporting bottleneck",
                "cover_letter": "Your team needs faster, more trusted analytics. I’ve solved that exact reporting bottleneck with React dashboards and API integration work.",
                "rationale": "Frames the client pain before the proof.",
                "match_notes": ["Leads with the reporting problem", "Connects to prior dashboard outcome"],
            },
        ],
        review_payloads=[
            {
                "structure": "concise",
                "final_headline": "React dashboard delivery",
                "final_cover_letter": "I’ve shipped React reporting systems for B2B SaaS teams and can own this rebuild end to end. I’d start by tightening data flows and the slowest UI paths.",
                "final_rationale": "Keeps the concise structure while adding a specific first-step signal.",
                "final_match_notes": ["React + dashboard fit", "Specific first-step plan"],
                "self_check_notes": ["Added a concrete first-step statement"],
            },
            {
                "structure": "problem-solution",
                "final_headline": "Fix the reporting bottleneck",
                "final_cover_letter": "Your team needs faster, more trusted analytics. I’ve solved that exact reporting bottleneck with React dashboards, API integration work, and measurable delivery outcomes.",
                "final_rationale": "Strengthened the proof while preserving the problem-solution flow.",
                "final_match_notes": ["Problem-led framing", "Portfolio evidence attached"],
                "self_check_notes": ["Tightened the evidence sentence"],
            },
        ],
    )

    original_factory = generation_route.get_cover_letter_generation_service
    generation_route.get_cover_letter_generation_service = lambda: CoverLetterGenerationService(
        draft_model_factory=factory,
        review_model_factory=factory,
        job_analysis_service=FakeJobAnalysisService(),
    )

    raw_job_text = """
We need a senior React engineer to rebuild our B2B SaaS analytics dashboard.
You should be comfortable with TypeScript, API integrations, and performance tuning.
This project is urgent and we want someone who can operate independently.
""".strip()

    try:
        response = client.post(
            "/generate",
            headers=headers,
            json={"raw_job_text": raw_job_text},
        )
    finally:
        generation_route.get_cover_letter_generation_service = original_factory

    assert response.status_code == 201
    body = response.json()
    assert body["prompt_version"] == "2026-05-20.phase-8.v1"
    assert [item["structure"] for item in body["variants"]] == ["concise", "problem-solution"]
    assert len(body["variants"]) == 2
    assert body["analysis"]["title"] == ANALYSIS.title

    stmt = (
        select(CoverLetterGenerationRun)
        .where(CoverLetterGenerationRun.id == uuid.UUID(body["id"]))
        .options(selectinload(CoverLetterGenerationRun.variants))
    )
    run = await db_session.scalar(stmt)
    assert run is not None
    assert run.analysis_snapshot_id == uuid.UUID(body["analysis_snapshot_id"])
    assert run.requested_structures == ["concise", "problem-solution"]
    assert run.graph_state["analysis"]["fit_score"] == 88
    assert run.graph_state["review_prompt_version"] == "2026-05-20.phase-8.review-v1"
    assert run.graph_state["feedback_memory_context"] == "No past feedback memory is available yet."
    assert len(run.variants) == 2
    assert run.variants[0].self_check_notes == ["Added a concrete first-step statement"]
    assert len(factory.calls) == 4


@pytest.mark.asyncio
async def test_generate_can_reuse_existing_analysis_snapshot(db_session):
    headers, user_id = _register_user()
    await _seed_profile_and_library(db_session, user_id)

    snapshot = JobAnalysisSnapshot(
        user_id=user_id,
        raw_job_text="Existing analyzed post",
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
    db_session.add(snapshot)
    await db_session.commit()
    await db_session.refresh(snapshot)

    factory = FakeStructuredFactory(
        draft_payloads=[
            {
                "structure": "consultative",
                "headline": "Start with the reporting bottleneck",
                "cover_letter": "Before writing code, I’d map the current reporting path and isolate where trust or speed is breaking for users.",
                "rationale": "Consultative tone fits the urgency and ambiguity.",
                "match_notes": ["Senior advisory framing"],
            }
        ],
        review_payloads=[
            {
                "structure": "consultative",
                "final_headline": "Start with the reporting bottleneck",
                "final_cover_letter": "Before writing code, I’d map the current reporting path and isolate where trust or speed is breaking for users. Then I’d sequence the rebuild around the highest-friction screens first.",
                "final_rationale": "Preserves the consultative structure and sharpens the plan.",
                "final_match_notes": ["Senior advisory framing", "Explicit phased plan"],
                "self_check_notes": ["Added phased execution detail"],
            }
        ],
    )

    original_factory = generation_route.get_cover_letter_generation_service
    generation_route.get_cover_letter_generation_service = lambda: CoverLetterGenerationService(
        draft_model_factory=factory,
        review_model_factory=factory,
    )

    try:
        response = client.post(
            "/generate",
            headers=headers,
            json={
                "analysis_snapshot_id": str(snapshot.id),
                "structures": ["consultative"],
            },
        )
    finally:
        generation_route.get_cover_letter_generation_service = original_factory

    assert response.status_code == 201
    body = response.json()
    assert body["analysis_snapshot_id"] == str(snapshot.id)
    assert [item["structure"] for item in body["variants"]] == ["consultative"]


def test_generate_requires_job_text_or_analysis_snapshot():
    headers, _ = _register_user()
    response = client.post("/generate", headers=headers, json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_retrieves_relevant_feedback_memory(db_session):
    headers, user_id = _register_user()
    await _seed_profile_and_library(db_session, user_id)

    snapshot = JobAnalysisSnapshot(
        user_id=user_id,
        raw_job_text="Urgent SaaS dashboard rebuild with React and TypeScript.",
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
    prior_run = CoverLetterGenerationRun(
        user_id=user_id,
        analysis_snapshot=snapshot,
        raw_job_text=snapshot.raw_job_text,
        requested_structures=["concise"],
        prompt_version="prior-run",
        graph_state={},
    )
    prior_variant = CoverLetterGenerationVariant(
        structure="concise",
        headline="Lead with dashboard pain",
        cover_letter="I would open by naming the reporting bottleneck and the KPI trust issue.",
        rationale="Pain-first opener converted better.",
        match_notes=["Pain-led framing"],
        self_check_notes=[],
        sort_order=0,
    )
    prior_run.variants.append(prior_variant)
    db_session.add(prior_run)
    await db_session.flush()

    memory_text = build_feedback_memory_text(
        variant=prior_variant,
        rating=5,
        edited_cover_letter="Start by naming the reporting bottleneck and the KPI trust issue.",
        accepted_sections=["Lead with the reporting bottleneck"],
        rejected_sections=["Avoid generic excitement"],
        client_response_outcome="hired",
        notes="Pain-first opening with KPI proof converted best.",
    )
    db_session.add(
        CoverLetterFeedback(
            user_id=user_id,
            generation_run_id=prior_run.id,
            generation_variant_id=prior_variant.id,
            rating=5,
            edited_cover_letter="Start by naming the reporting bottleneck and the KPI trust issue.",
            accepted_sections=["Lead with the reporting bottleneck"],
            rejected_sections=["Avoid generic excitement"],
            client_response_outcome="hired",
            notes="Pain-first opening with KPI proof converted best.",
            memory_text=memory_text,
            memory_embedding=embed_text(memory_text),
        )
    )
    await db_session.commit()

    factory = FakeStructuredFactory(
        draft_payloads=[
            {
                "structure": "concise",
                "headline": "Dashboard bottleneck fix",
                "cover_letter": "I would start by isolating the reporting bottleneck, then rebuild the slowest dashboard flows with measurable KPI proof.",
                "rationale": "Uses the proven pain-first pattern.",
                "match_notes": ["Reflects prior winning opener"],
            }
        ],
        review_payloads=[
            {
                "structure": "concise",
                "final_headline": "Dashboard bottleneck fix",
                "final_cover_letter": "I would start by isolating the reporting bottleneck, then rebuild the slowest dashboard flows with measurable KPI proof and a phased delivery plan.",
                "final_rationale": "Keeps the proven pain-first opener and strengthens execution detail.",
                "final_match_notes": ["Pain-first opener", "Execution detail"],
                "self_check_notes": ["Preserved prior accepted pattern"],
            }
        ],
    )

    original_factory = generation_route.get_cover_letter_generation_service
    generation_route.get_cover_letter_generation_service = lambda: CoverLetterGenerationService(
        draft_model_factory=factory,
        review_model_factory=factory,
    )

    try:
        response = client.post(
            "/generate",
            headers=headers,
            json={
                "analysis_snapshot_id": str(snapshot.id),
                "structures": ["concise"],
            },
        )
    finally:
        generation_route.get_cover_letter_generation_service = original_factory

    assert response.status_code == 201
    draft_messages = "\n".join(factory.calls[0]["messages"])
    assert "Lead with the reporting bottleneck" in draft_messages
    assert "Avoid generic excitement" in draft_messages
