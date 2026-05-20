# infra

Local development infrastructure.

## Start dependencies

```bash
cd infra
docker compose up -d
```

Brings up:

- **PostgreSQL 16** (with `pgvector`) on `localhost:5432` — db `cover_letter`, user `postgres`, password `postgres`
- **Redis 7** on `localhost:6379` — used by Celery, request rate limits, and caching layers

## Run the API and worker locally

In separate terminals:

```bash
cd apps/api
uv run uvicorn app.main:app --reload --port 8000
```

```bash
cd apps/api
uv run celery -A app.worker.celery_app worker --loglevel=info
```

## Stop

```bash
docker compose down            # keep data
docker compose down -v         # also remove volumes
```
