# API — Upwork Cover Letter AI SaaS

FastAPI backend that powers the SaaS. PostgreSQL is the source of truth; LangChain/LangGraph drives generation; Celery + Redis handles async work.

## Local development

```bash
cd apps/api
uv venv
uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8080
```

Health probe:

```bash
curl http://localhost:8000/health
```

## Layout

```
app/
  core/      # config, db engine, security, dependencies
  api/       # route modules (auth, profile, generator, ...)
  models/    # SQLAlchemy ORM models
  schemas/   # Pydantic request/response schemas
  services/  # domain services, LangGraph integrations
alembic/     # database migrations
tests/       # pytest test suite
```

## Tests

```bash
uv run pytest -q
```
