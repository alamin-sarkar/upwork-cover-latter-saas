# Deployment Runbook

## Scope
This runbook covers the production deployment shape introduced in Phase 11:
- FastAPI API container from `apps/api/Dockerfile`
- Next.js web container from `apps/web/Dockerfile`
- PostgreSQL with `pgvector`
- Redis for Celery broker/result backend and rate-limit counters
- Celery worker process using `app.worker:celery_app`

## Required environment
- `ENVIRONMENT=production`
- `DOCS_ENABLED=false`
- `JWT_SECRET` set to a unique secret with at least 32 characters
- `ADMIN_DIAGNOSTICS_TOKEN` set to a unique secret with at least 16 characters
- `DATABASE_URL` pointed at the production PostgreSQL instance
- `REDIS_URL` pointed at the production Redis instance
- `ANTHROPIC_API_KEY` configured if job analysis and generation should be live
- Optional: `CELERY_RESULT_BACKEND` if you do not want to reuse `REDIS_URL`

## Build images
From the repo root:

```bash
docker build -f apps/api/Dockerfile -t pitchcraft-api .
docker build -f apps/web/Dockerfile -t pitchcraft-web .
```

## Start order
1. Start PostgreSQL and Redis first.
2. Run database migrations:

```bash
cd apps/api
uv run alembic upgrade head
```

3. Start the API container.
4. Start one or more Celery worker processes:

```bash
cd apps/api
uv run celery -A app.worker.celery_app worker --loglevel=info
```

5. Start the web container after the API base URL is reachable.

## Verification checklist
Run these checks after deployment:

```bash
curl https://<api-host>/health
curl https://<api-host>/health/ready
curl -H "X-Admin-Token: <token>" https://<api-host>/admin/diagnostics
```

Expected signals:
- `/health` returns `status=ok`
- `/health/ready` returns HTTP `200` with database and Redis `ok=true`
- `/admin/diagnostics` returns the current request id, dependency status, configured rate limits, and Celery worker visibility

## Rollback
1. Roll back the API and web images to the last known good tag.
2. If the issue is migration-related, restore the database from backup before downgrading schema manually.
3. Re-run the verification checklist.

## CI parity
GitHub Actions runs:
- API migration upgrade
- API lint + test
- Web lint + build + typecheck

Do not deploy from a branch whose CI run is red.
