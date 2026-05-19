# API Service (FastAPI)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Health check
- `GET /health`

## Alembic
```bash
alembic upgrade head
```
