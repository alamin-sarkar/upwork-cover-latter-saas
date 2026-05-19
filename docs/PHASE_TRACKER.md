# Phase Tracker

> **Read this first when the user says "porer phase shuru koro" / "continue next phase".**
> This file is the single source of truth for what's done, what's next, and the acceptance criteria for each phase. After completing a phase, flip its status here AND add an entry in `BUILD_LOG.md`.

**Build cadence:** one phase per run (per `AGENTS.md`). Do not skip phases. If a phase is too large, split it into numbered sub-milestones inside this file before starting.

---

## Status legend
- `[x] DONE` — shipped, tests pass, committed
- `[~] IN PROGRESS` — partially shipped, see notes
- `[ ] TODO` — not started
- `[!] BLOCKED` — waiting on external input (note the blocker)

## Current pointer
**Next phase to start:** **Phase 3 — Auth + user/plan models**

When you (Claude) resume:
1. Read this file's "Current pointer" line.
2. Read the matching phase section below for scope + acceptance criteria.
3. Read the latest entry in `BUILD_LOG.md` for context on what just shipped.
4. Confirm scope with user only if something is ambiguous; otherwise start.
5. After shipping: update the phase checkbox here, move the "Current pointer", append to `BUILD_LOG.md`, commit.

---

## Phase 1 — Repo bootstrap + baseline scaffolding  `[x] DONE` (2026-05-19)
**Scope:** monorepo skeleton, baseline configs, design handoff archived.
**Delivered:**
- `apps/api/` FastAPI + `/health` + pytest scaffold + full prod dependency set
- `apps/web/` Next.js 15 + Tailwind theme (PitchCraft forest palette)
- `packages/ai-workflows/` empty Python package
- `infra/docker-compose.yml` Postgres+pgvector + Redis
- `docs/design-handoff/` archived; `docs/BUILD_LOG.md` started
**Acceptance:** scaffolding compiles; `git status` clean after commit. ✅

---

## Phase 2 — FastAPI core + Postgres migrations  `[x] DONE` (2026-05-19)
**Scope:**
- `app/core/db.py` — SQLAlchemy 2 async engine + `SessionLocal` + `get_db` dependency
- `app/core/deps.py` — common FastAPI dependencies
- `app/core/security.py` — password hashing (passlib/bcrypt) + JWT encode/decode helpers (no routes yet)
- Alembic init: `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`
- `alembic/versions/0001_baseline.py` — empty baseline (creates `alembic_version` only) OR enables `pgvector` extension
- `tests/conftest.py` — test DB fixture (sqlite-in-memory or a `pytest-postgresql` ephemeral DB)
- Smoke test that `get_db` yields a session and rolls back
**Acceptance:**
- `alembic upgrade head` runs cleanly against the docker-compose Postgres
- `pytest -q` passes (`test_health` + new db smoke test)
- No models defined yet (they belong to Phase 3+)

---

## Phase 3 — Auth + user/plan models  `[ ] TODO`
**Scope:**
- `app/models/user.py` — `User`, `Plan` enum (free/pro/team), audit timestamps
- `app/schemas/auth.py`, `app/schemas/user.py`
- `app/api/routes/auth.py` — `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `GET /auth/me`
- Alembic migration `0002_users.py`
- `tests/test_auth.py` — register/login/refresh/me happy + sad paths
**Acceptance:** all 4 endpoints round-trip with JWT; refresh rotation works; password hashing uses bcrypt; tests pass.

---

## Phase 4 — Profile settings domain  `[ ] TODO`
**Scope:** normalized profile model: `profiles`, `profile_skills`, `profile_projects`, `profile_experiences`, `profile_niches`, `profile_custom_sections`, `profile_preferences`. CRUD routes scoped to the authenticated user. Migrations + tests.
**Acceptance:** authenticated user can create/read/update/delete each section; cascading deletes work; tests cover ownership isolation.

---

## Phase 5 — Guidelines / sample library domain  `[ ] TODO`
**Scope:** `cover_letter_guidelines`, `cover_letter_samples` (with tags: winning / anti-pattern), reusable intros/CTAs, tone presets. CRUD + tests.
**Acceptance:** user can manage guidelines and samples; samples support tagging; tests cover ownership.

---

## Phase 6 — Job post ingestion + structured analysis  `[ ] TODO`
**Scope:**
- `packages/ai-workflows/src/ai_workflows/job_analysis/` — prompts, Pydantic schemas, LangGraph node
- `app/services/job_analysis.py` — orchestrator using Anthropic SDK
- `app/api/routes/job_analysis.py` — `POST /jobs/analyze`
- Persisted snapshot model so analyses are auditable
- Tests with a mocked Anthropic client
**Acceptance:** posting raw job text returns structured `{title, scope, deliverables, required_skills, budget_clues, urgency, tone, risk_flags, fit_score}`.

---

## Phase 7 — Cover-letter generation graph  `[ ] TODO`
**Scope:**
- LangGraph workflow: normalize → analyze → retrieve profile evidence → retrieve guidelines/samples → draft N variants → self-check → return
- Five supported structures: concise / problem-solution / credibility-first / portfolio-first / consultative
- `POST /generate` returns multiple variants with rationale + match notes
- History persistence: raw inputs, analysis, drafts, prompt version
- Tests with mocked LLM
**Acceptance:** one job post → ≥2 distinct structured variants + rationale; every output is traceable to prompt version + profile inputs + analysis snapshot.

---

## Phase 8 — Feedback memory + adaptive improvement  `[ ] TODO`
**Scope:** rating, edited final text, accepted/rejected sections, client-response outcome. Feedback is fed back into next-run retrieval (pgvector for relevant past feedback). Tests cover memory recall.
**Acceptance:** feedback persists and visibly influences the next generation's prompt context.

---

## Phase 9 — Next.js dashboard + workflow screens  `[ ] TODO`
**Scope:** port the 6 design-handoff screens (`auth`, `dashboard`, `generator`, `history`, `knowledge`, `settings`) to Next.js App Router. Wire to the API with TanStack Query. Zustand for client state. Auth guard middleware. Match the PitchCraft forest palette.
**Acceptance:** end-to-end flow works in the browser — sign in → fill profile → paste a job → see analysis + drafts → save feedback → see it in history.

---

## Phase 10 — MCP integration layer  `[ ] TODO`
**Scope:** MCP server exposing profile, guidelines, samples, and a `generate_cover_letter` tool. Auth via per-user MCP token. Docs + a minimal MCP client smoke test.
**Acceptance:** external MCP client can list resources and invoke the generator tool successfully.

---

## Phase 11 — Usage limits, observability, deployment hardening  `[ ] TODO`
**Scope:** plan-based rate limiting, structured logging (structlog), request tracing hooks, admin diagnostics, Celery workers wired for async jobs, Dockerfiles for api + web, CI workflow (lint + test + build), production-ready `.env` validation, deployment runbook.
**Acceptance:** CI green; rate limits enforced; structured logs include request id; deployment runbook documented.

---

## Sub-milestone template (use if a phase needs splitting)
```
### Phase X.Y — <short name>  `[ ] TODO`
Scope: <one paragraph>
Files: <list>
Acceptance: <bullets>
```
