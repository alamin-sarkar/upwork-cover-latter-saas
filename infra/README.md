# infra

Local development infrastructure.

## Start dependencies

```bash
cd infra
docker compose up -d
```

Brings up:

- **PostgreSQL 16** (with `pgvector`) on `localhost:5432` — db `cover_letter`, user `postgres`, password `postgres`
- **Redis 7** on `localhost:6379` — used by Celery and caching layers

## Stop

```bash
docker compose down            # keep data
docker compose down -v         # also remove volumes
```
