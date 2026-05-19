# Build Log

Append a dated entry per completed milestone. Newest at the top.

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
