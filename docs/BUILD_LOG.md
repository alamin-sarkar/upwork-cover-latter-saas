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
- Next step:
  - Bootstrap Next.js TypeScript app shell in `apps/web`.
