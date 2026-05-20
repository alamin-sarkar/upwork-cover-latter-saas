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

