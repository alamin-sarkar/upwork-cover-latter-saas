# API — Upwork Cover Letter AI SaaS

FastAPI backend that powers the SaaS. PostgreSQL is the source of truth; LangChain/LangGraph drives generation; Celery + Redis handles async work.

## Local development

```bash
cd infra
docker compose up -d postgres redis

cd apps/api
uv venv
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

### Database init / migrations

- The app uses PostgreSQL from `infra/docker-compose.yml`; the DB is **not** auto-created from an in-memory fallback.
- If `RUN_MIGRATIONS_ON_STARTUP=true` (default in `.env.example`), FastAPI automatically runs pending Alembic migrations at startup.
- You can run the DB init manually anytime:

```bash
cd apps/api
uv run alembic upgrade head
```

- If Postgres is not running yet, startup and migrations will fail. Start `postgres` first from `infra/`.

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

## Runtime hardening

- Every HTTP response includes an `X-Request-ID` header.
- `/health/ready` verifies database and Redis readiness.
- `/admin/diagnostics` is protected by `X-Admin-Token` and reports dependency health, active rate-limit settings, and Celery worker visibility.
- Daily plan-based limits are enforced for job analysis and cover-letter generation.

## MCP integration

Create a per-user MCP token with your normal JWT session:

```bash
curl -X POST http://localhost:8000/mcp/tokens \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"label":"Claude Desktop"}'
```

Use the returned MCP token as a bearer token for JSON-RPC requests to `/mcp`:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Authorization: Bearer <mcp-token>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}'
```

Supported MCP methods in this phase:
- `initialize`
- `resources/list`
- `resources/read` for `pitchcraft://profile`, `pitchcraft://guidelines`, and `pitchcraft://samples`
- `tools/list`
- `tools/call` for `generate_cover_letter`

## Celery worker

Start a worker locally with:

```bash
uv run celery -A app.worker.celery_app worker --loglevel=info
```

Registered tasks:
- `pitchcraft.job_analysis.analyze_post`
- `pitchcraft.cover_letters.generate`
- `pitchcraft.worker.ping`
