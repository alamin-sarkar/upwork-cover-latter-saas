# Build Log

## 2026-05-19 11:02 (Asia/Dhaka)
- Completed micro-milestone: Monorepo skeleton setup.
- Created directories:
  - `apps/web`
  - `apps/api`
  - `packages/ai-workflows`
  - `infra`
  - `.github/workflows`
- Added placeholder tracking files (`.gitkeep`) for clean Git structure.
- Validation:
  - Verified directory structure exists.

## 2026-05-19 11:08 (Asia/Dhaka)
- Completed micro-milestone: FastAPI bootstrap + PostgreSQL config scaffold + health endpoint + Alembic baseline.
- Added under `apps/api`:
  - `pyproject.toml` (FastAPI, SQLAlchemy, Alembic, psycopg, pytest)
  - `.env.example` (PostgreSQL connection scaffold)
  - `app/core/config.py`, `app/core/db.py`, `app/main.py`
  - `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`, `alembic/versions/0001_baseline.py`
  - `tests/test_health.py`, `README.md`
- Validation:
  - `pytest -q` => `1 passed`

## 2026-05-19 11:14 (Asia/Dhaka)
- Completed micro-milestone: Next.js + TypeScript + base auth shell scaffold.
- Added under `apps/web`:
  - Next.js app bootstrap (App Router, TypeScript, Tailwind, ESLint)
  - Home page with Login/Register navigation
  - `src/app/login/page.tsx`
  - `src/app/register/page.tsx`
- Validation:
  - `npm run lint` => pass
  - `npm run build` => pass
- Next step:
  - Implement JWT auth endpoints and user/plan schema in backend.

## 2026-05-19 11:52 (Asia/Dhaka)
- Completed planning/doc-alignment milestone for product repositioning.
- Reframed the project from interview copilot direction to **Upwork Cover Letter AI SaaS**.
- Updated root planning/agent files:
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `MEMORY.md`
  - `docs/MASTER_PLAN.md`
  - `docs/plans/2026-05-19-upwork-cover-letter-saas-implementation-plan.md`
- Established domain scope for:
  - structured user profile sections
  - writing guidelines and sample letters
  - job-post analysis
  - multi-structure cover-letter generation
  - feedback memory and history
  - MCP integration
- Validation:
  - reviewed repository state
  - ensured doc changes are additive and do not disturb in-progress auth backend files
- Next step:
  - Finish backend auth milestone already in progress before building profile/settings domain.

## 2026-05-19 13:30 (Asia/Dhaka)
- Completed micro-milestone: backend auth foundation.
- Added backend auth domain under `apps/api`:
  - `app/api/routes/auth.py` for register, login, refresh, and current-user endpoints
  - `app/core/security.py` for password hashing and JWT issuance/verification
  - `app/core/deps.py` for DB session and bearer-token current-user resolution
  - `app/models/user.py` and `app/models/__init__.py` for user, role, and plan persistence
  - `app/schemas/auth.py`, `app/schemas/user.py`, and package exports for request/response contracts
- Updated bootstrap files:
  - `app/main.py` to mount auth routes
  - `app/core/config.py` and `.env.example` for JWT settings
  - `alembic/versions/0001_baseline.py` to create the users table
  - `pyproject.toml` for auth-related dependencies
  - `apps/api/README.md` with auth endpoint and run/test instructions
- Added TDD coverage:
  - `tests/test_auth.py` for register, duplicate email rejection, login, invalid password rejection, `/me`, refresh, and refresh token misuse
- Validation:
  - `.venv/bin/python -m pytest -q` => `8 passed`
- Next step:
  - Build authenticated profile/settings module on top of this auth base.
