# CLAUDE.md — Project Build Contract

## Product
Interview Copilot SaaS: CV-JD match analysis, AI-generated mock interviews, answer scoring, improvement suggestions, progress dashboard.

## Non-Negotiables
- Production-minded code quality from day 1
- Security basics enabled early (auth, rate limit, validation)
- Postgres-first schema design
- LangChain/LangGraph orchestration for AI flows
- Clear boundaries: frontend/backend/ai-workflow/domain

## Tech Decisions
- Frontend: Next.js (App Router), TypeScript, React, Tailwind, TanStack Query
- Backend: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2
- DB: PostgreSQL
- Queue: Celery + Redis
- Auth: JWT access/refresh
- Tests: Pytest + Playwright (frontend e2e later)

## Build Sequence (high level)
1. Repo bootstrap + monorepo structure
2. FastAPI core + Postgres migrations
3. Auth + user/plan models
4. Resume/JD ingestion APIs
5. LangChain match analysis flow
6. LangGraph interview pipeline
7. Next.js app screens + API integration
8. Usage limits/billing hooks
9. Observability + hardening + deployment

## Quality Gate
No milestone is complete without tests + docs + commit.
