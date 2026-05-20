# Build Log

Append a dated entry per completed milestone. Newest at the top.

---

## 2026-05-20 — Phase 9: Next.js dashboard and workflow screens

**Scope:** replace the single-page web prototype with a routed App Router frontend wired to the live API for auth, settings, generation, feedback history, and knowledge management.

**Delivered:**
- `apps/web/src/app/auth/page.tsx` — real sign-in / register screen that calls the FastAPI auth endpoints, stores the JWT session, and redirects into the workspace.
- `apps/web/middleware.ts` + `src/lib/auth.ts` + `src/lib/auth-store.ts` — cookie-backed auth guard middleware, persisted Zustand session state, and shared token helpers for protected routes.
- `apps/web/src/components/providers.tsx` + `src/lib/query-client.ts` — TanStack Query provider setup for API-driven screens.
- `apps/web/src/components/workspace-shell.tsx` + `src/app/(workspace)/layout.tsx` — protected app shell with routed navigation for dashboard, generator, history, knowledge, and settings.
- `apps/web/src/app/(workspace)/dashboard/page.tsx` — live dashboard using feedback and profile queries to summarize readiness and recent outcomes.
- `apps/web/src/app/(workspace)/generator/page.tsx` — end-to-end generator flow: analyze job, generate variants, select a draft, and save feedback memory.
- `apps/web/src/app/(workspace)/history/page.tsx` — feedback timeline showing saved outcomes, accepted sections, and rejected patterns.
- `apps/web/src/app/(workspace)/knowledge/page.tsx` — CRUD entry screens for guidelines and cover-letter samples.
- `apps/web/src/app/(workspace)/settings/page.tsx` — profile, preferences, skills, and project management wired to the profile domain.
- `apps/web/src/app/page.tsx` + `src/lib/api-client.ts` — root redirect based on session cookies and typed API client updates for authenticated requests.

**Verification:** `npm ci` ✅ · `npm run lint` ✅ · `npm run build` ✅ · `npm run typecheck` ✅

**Notes:** `tsconfig.json` depends on `.next/types`, so standalone `npm run typecheck` must run after a successful `next build` in this repo.

**Next milestone:** Phase 10 — MCP integration layer.

## 2026-05-20 — Phase 8: Feedback memory and adaptive improvement

**Scope:** persist post-generation feedback signals, retrieve relevant prior feedback with pgvector-backed memory search, and feed that context into the next cover-letter generation run.

**Delivered:**
- `apps/api/app/models/feedback.py` + `alembic/versions/0007_feedback_memory.py` — `cover_letter_feedback` table with user ownership, one-feedback-per-variant enforcement, edited final text, accepted/rejected sections, client outcome, and a pgvector embedding column for retrieval.
- `apps/api/app/api/routes/feedback.py` + `app/schemas/feedback.py` — authenticated feedback endpoints for create, list, get, and update flows under `/history/feedback`.
- `apps/api/app/services/feedback_memory.py` — deterministic local embedding generation, feedback memory text synthesis, ownership-safe variant lookup, and relevant-memory retrieval ordered by vector cosine distance.
- `packages/ai-workflows/src/ai_workflows/generation/graph.py` + `generation/prompts.py` — added a feedback-memory retrieval step to the LangGraph workflow and upgraded generation/review prompts so drafts adapt to accepted and rejected patterns from past outcomes.
- `apps/api/app/services/generation.py` — feedback memory is now injected into every generation run and persisted in the stored graph state for auditability.
- `apps/api/tests/test_feedback.py` + `tests/test_generation.py` — CRUD coverage for the feedback API, duplicate protection, ownership isolation, and proof that saved feedback memory appears in the next generation prompt context.

**Verification:** `uv run alembic upgrade head` ✅ · `uv run pytest -q tests/test_feedback.py` ✅ · `uv run pytest -q tests/test_generation.py` ✅ · `uv run pytest -q tests/test_job_analysis.py` ✅ · `uv run ruff check app tests` ✅

**Next milestone:** Phase 9 — Next.js dashboard + workflow screens.

## 2026-05-20 — Phase 7: Cover-letter generation graph

**Scope:** LangGraph-based cover-letter agent workflow with LangChain structured generation, persisted run history, multiple structure styles, and per-run state memory.

**Delivered:**
- `packages/ai-workflows/src/ai_workflows/generation/` — shared generation schemas, LangChain prompt templates, structure guidance for the 5 supported letter styles, and a LangGraph state machine with checkpoint-backed run memory.
- `apps/api/app/services/generation.py` — `CoverLetterGenerationService` that runs the graph end to end: normalize input, reuse or create analysis, retrieve profile evidence, retrieve guidelines/samples, draft variants, self-check variants, and persist the final graph state plus output history.
- `apps/api/app/api/routes/generation.py` + `app/schemas/generation.py` — authenticated `POST /generate` endpoint that returns multiple structured variants, rationale, match notes, and the linked analysis snapshot.
- `apps/api/app/models/generation.py` + `alembic/versions/0006_generation.py` — `cover_letter_generation_runs` and `cover_letter_generation_variants` tables for auditable history of raw job input, requested structures, prompt version, graph state, and final drafts.
- `apps/api/pyproject.toml` — added `langchain-anthropic` and switched the local `ai-workflows` package source to editable mode so shared workflow code resolves cleanly from the monorepo.
- `apps/api/tests/test_generation.py` — mocked LangChain model coverage for multi-variant generation, persisted run state, and reusing an existing analysis snapshot.

**Verification:** `uv sync --reinstall-package ai-workflows` ✅ · `uv run alembic upgrade head` ✅ · `uv run ruff check app tests` ✅ · `uv run pytest -q` → 51 passed ✅

**Notes:** this phase adds stateful LangGraph run memory and persisted generation state. Cross-run adaptive feedback memory remains Phase 8 and was not bundled into this delivery.

**Next milestone:** Phase 8 — Feedback memory + adaptive improvement.

---

## 2026-05-20 — Phase 6: Job post ingestion and structured analysis

**Scope:** shared job-analysis workflow contract, Anthropic-backed structured extraction, persisted audit snapshots, and an authenticated analysis endpoint.

**Delivered:**
- `packages/ai-workflows/src/ai_workflows/job_analysis/` — prompt versioning, structured `JobAnalysis` schema, and a small LangGraph state wrapper for analysis execution.
- `apps/api/app/models/job_analysis.py` — `JobAnalysisSnapshot` ORM model that stores the raw post, normalized fields, provider metadata, and the full structured payload for auditability.
- `apps/api/app/services/job_analysis.py` — `JobAnalysisService` orchestrator that calls Anthropic, validates the JSON response against the shared schema, runs through the LangGraph node, and persists the snapshot.
- `apps/api/app/api/routes/job_analysis.py` + `app/schemas/job_analysis.py` — authenticated `POST /jobs/analyze` request/response contract with clear `503` handling when the provider is not configured.
- `apps/api/alembic/versions/0005_job_analysis.py` — creates `job_analysis_snapshots` with ownership index and check constraints for `fit_score`, `urgency`, and `tone`.
- `apps/api/tests/test_job_analysis.py` — mocked-Anthropic coverage proving structured response shape, persistence, and payload validation behavior.
- `apps/api/pyproject.toml` — wired the local `ai-workflows` package into the API environment as a real dependency instead of a path hack.

**Verification:** `uv sync` ✅ · `uv run alembic upgrade head` ✅ · `uv run ruff check app tests` ✅ · `uv run pytest -q` → 48 passed ✅

**Next milestone:** Phase 7 — Cover-letter generation graph.

---

## 2026-05-20 — Phase 5: Guidelines and sample library domain

**Scope:** authenticated CRUD for a user-owned cover-letter playbook with reusable rules, intros, CTAs, tone presets, and tagged sample letters.

**Delivered:**
- `app/models/library.py` — `CoverLetterGuideline` and `CoverLetterSample` ORM models with direct user ownership, ordering, and audit timestamps.
- `app/schemas/library.py` — typed request/response contracts, including validated guideline types (`rule`, `intro`, `cta`, `tone_preset`) and sample tags (`winning`, `anti-pattern`).
- `app/api/routes/library.py` — authenticated CRUD for guidelines and samples, plus list filtering by `guideline_type` and `tag`.
- `app/api/router.py` + `app/models/__init__.py` — registered the library routes and exported the new models for metadata discovery.
- `alembic/versions/0004_library.py` — creates the `cover_letter_guidelines` and `cover_letter_samples` tables with ownership indexes, `ON DELETE CASCADE`, and check constraints for valid type/tag values.
- `tests/test_library.py` — CRUD, invalid payload, filter, and ownership-isolation coverage for the new domain.

**Verification:** `uv run alembic upgrade head` ✅ · `uv run ruff check app tests` ✅ · `uv run pytest -q` → 46 passed ✅

**Next milestone:** Phase 6 — Job post ingestion + structured analysis.

---

## 2026-05-20 — Phase 4: Profile settings domain

**Scope:** normalized profile aggregate, user-scoped CRUD, migration, and ownership tests.

**Delivered:**
- `app/models/profile.py` — `Profile`, `ProfileSkill`, `ProfileProject`, `ProfileExperience`, `ProfileNiche`, `ProfileCustomSection`, and `ProfilePreferences` ORM models with ordered child relationships and delete cascading.
- `app/models/user.py` + `app/models/__init__.py` — wired one-to-one user ↔ profile relationship and model exports for Alembic metadata.
- `app/schemas/profile.py` — Pydantic request/response contracts for the profile aggregate, each section collection, and singleton preferences.
- `app/api/routes/profile.py` — authenticated CRUD for profile root, skills, projects, experiences, niches, custom sections, and preferences. Child section creation auto-creates the owning profile when needed.
- `app/api/router.py` — profile routes registered.
- `alembic/versions/0003_profiles.py` — creates all Phase 4 tables and indexes with `ON DELETE CASCADE` foreign keys.
- `tests/test_profile.py` — CRUD, validation, ownership isolation, and cascade-delete coverage for the new domain.

**Verification:** `uv run alembic upgrade head` ✅ · `uv run ruff check app tests` ✅ · `uv run pytest -q` → 34 passed ✅

**Notes:** local verification required starting the repo's Docker Postgres/Redis stack from `infra/docker-compose.yml` because nothing was listening on `localhost:5432`.

**Next milestone:** Phase 5 — Guidelines / sample library domain (guidelines, reusable intros/CTAs, tone presets, tagged samples).

---

## 2026-05-19 — Phase 3: Auth + user/plan models

**Scope:** JWT auth system with register, login, refresh, and me endpoints.

**Delivered:**
- `app/models/base.py` — SQLAlchemy 2 `DeclarativeBase`.
- `app/models/user.py` — `User` ORM model + `Plan` enum (free/pro/team), audit timestamps.
- `app/schemas/auth.py` — `RegisterRequest`, `LoginRequest`, `TokenResponse`, `RefreshRequest` (Pydantic v2).
- `app/schemas/user.py` — `UserOut` (from_attributes=True).
- `app/api/routes/auth.py` — `POST /auth/register` (201), `POST /auth/login`, `POST /auth/refresh` (stateless rotation), `GET /auth/me`.
- `app/api/router.py` — top-level API router; include_router wired into `main.py`.
- `app/core/deps.py` — added `get_current_user` (HTTPBearer → JWT decode → User lookup) + `CurrentUser` alias.
- `alembic/env.py` — `target_metadata = Base.metadata` wired for autogenerate from Phase 4+.
- `alembic/versions/0002_users.py` — creates `plan` enum (idempotent DO block) + `users` table + unique index on email.
- `tests/test_auth.py` — 15 auth tests covering all 4 endpoints, happy + sad paths.

**Fixes applied during this phase:**
- `passlib 1.7.x` is incompatible with `bcrypt 4+/5+` — replaced with direct `bcrypt` library; removed passlib from deps.
- `sa.Enum` ignores `create_type=False` — switched migration to `sqlalchemy.dialects.postgresql.ENUM`.
- `email-validator` rejects reserved TLDs (`.test`, `.local`) — test emails use `@acme.com`.
- FastAPI 0.115+ `HTTPBearer` returns 401 (not 403) for missing credentials — test updated.

**Verification:** `alembic upgrade head` ✅ · `pytest -q` → 19 passed ✅

**Next milestone:** Phase 4 — Profile settings domain (skills, projects, experiences, niches, preferences CRUD).

---

## 2026-05-19 — Phase 2: FastAPI core + Postgres migrations

**Scope:** async DB engine wiring, Alembic init, pgvector baseline migration, security helpers.

**Delivered:**
- `apps/api/app/core/db.py` — SQLAlchemy 2 async engine (`postgresql+psycopg_async://`), `SessionLocal` (`async_sessionmaker`), `get_db` async generator with automatic rollback on error.
- `apps/api/app/core/deps.py` — `DbSession` `Annotated` alias for `Depends(get_db)`; placeholder comment for `CurrentUser` (Phase 3).
- `apps/api/app/core/security.py` — `hash_password` / `verify_password` (passlib bcrypt), `create_access_token` / `create_refresh_token` / `decode_token` (python-jose HS256).
- `apps/api/alembic.ini` + `alembic/env.py` — async-aware Alembic setup; Windows `SelectorEventLoop` policy applied so psycopg3 async works on Windows.
- `apps/api/alembic/versions/0001_baseline.py` — enables the `vector` (pgvector) extension.
- `apps/api/alembic/script.py.mako` — migration template.
- `apps/api/tests/conftest.py` — `db_session` fixture (async, per-test, auto-rollback).
- `apps/api/tests/test_db_smoke.py` — 3 smoke tests: session type check, `SELECT 1`, rollback + re-query.

**Verification:**
- `alembic upgrade head` → `Running upgrade  -> 0001, baseline: enable pgvector extension` ✅
- `pytest -q` → 4 passed (test_health × 1 + db smoke × 3) ✅

**Known quirk:** Windows `ProactorEventLoop` is incompatible with psycopg3 async. Fixed in both `alembic/env.py` and `tests/conftest.py` by setting `WindowsSelectorEventLoopPolicy` before the loop is created.

**Next milestone:** Phase 3 — Auth + user/plan models (User ORM, Plan enum, register/login/refresh/me endpoints, Alembic migration 0002).

---

## 2026-05-19 — Phase 1: Repo bootstrap + baseline scaffolding

**Scope:** restore the monorepo skeleton after `9458b26 del old` cleared the working tree.

**Delivered:**
- `apps/api/` — FastAPI bootstrap with `/health` endpoint, `pydantic-settings` config, `.env.example`, pyproject with the production dependency set (FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, Anthropic SDK, LangChain/LangGraph, Celery, Redis, pgvector), pytest scaffold, and one health-endpoint test.
- `apps/web/` — Next.js 15 (App Router) + TypeScript + Tailwind shell. Tailwind theme tokens map the PitchCraft "forest" palette from `docs/design-handoff/` (dark base + Upwork green accent). One placeholder landing page renders the brand and call-out.
- `packages/ai-workflows/` — empty Python package scaffold (will be filled in Phases 6–8).
- `infra/docker-compose.yml` — PostgreSQL 16 + pgvector and Redis 7 services for local development.
- `docs/BUILD_LOG.md` — this log.

**Out of scope (deferred to later phases):**
- Database models, migrations, Alembic config (Phase 2)
- Auth (Phase 3)
- Profile, knowledge, generation, history, MCP, observability (Phases 4–11)

**Verification:** scaffolding only; no runnable cross-service tests yet. `pytest -q` inside `apps/api` is wired to pass against the health endpoint once dependencies are installed.

**Next milestone:** Phase 2 — FastAPI core hardening (db engine, dependency wiring, Alembic init, baseline migration).
