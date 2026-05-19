# Interview Copilot SaaS

Production-grade AI SaaS for CV↔JD matching and mock interview coaching (Bangla + English).

## Planned Stack
- Frontend: Next.js (App Router), React, TypeScript, Tailwind
- Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL
- AI: LangChain + LangGraph (provider-agnostic)
- Infra: Docker Compose, Redis/Celery (async), GitHub Actions CI

## Current Status
- ✅ Project blueprint created
- ✅ Execution plan created
- ✅ Agent orchestration docs created (`AGENTS.md`, `CLAUDE.md`)
- ⏳ Incremental implementation in small chunks via scheduled autonomous runs

## Quick Start (will be activated as implementation lands)
```bash
git clone <repo-url>
cd interview-copilot-saas
cp .env.example .env
docker compose up -d
```

## Principles
- Small batch changes (5-hour safe)
- One milestone per run
- Commit after each completed chunk
- No placeholder/dummy code in main branch
