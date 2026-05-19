# Interview Copilot SaaS — Bulletproof A→Z Plan

## Goal
Build and ship a 100% working, production-quality AI SaaS using Next.js + TypeScript + React (frontend), FastAPI + PostgreSQL (backend), and LangChain/LangGraph (AI orchestration), with incremental autonomous execution.

## Monorepo Layout
- `apps/web` — Next.js frontend
- `apps/api` — FastAPI backend
- `packages/ai-workflows` — LangChain/LangGraph flows/prompts/parsers
- `infra/` — docker compose, deployment, CI assets
- `docs/` — architecture, ADRs, API contracts, runbooks

## Phase Plan (small chunks)
### Phase 0: Foundation
- Initialize monorepo
- Tooling baseline (lint, format, pre-commit)
- Docker compose (postgres, redis)

### Phase 1: Backend Core
- FastAPI app factory, config system
- SQLAlchemy models + Alembic baseline
- Health/readiness/liveness endpoints

### Phase 2: Identity & Access
- Register/login/refresh/me
- JWT strategy + password hashing
- Role/plan enums

### Phase 3: Domain APIs
- Resumes CRUD + parsing pipeline
- Job Descriptions CRUD
- Match request + result retrieval

### Phase 4: AI Workflows
- LangChain prompt templates + output parser
- Match scoring chain
- LangGraph interview flow (generate→answer→evaluate→report)

### Phase 5: Frontend App
- Auth screens
- Resume/JD management screens
- Match report UI
- Mock interview session UI
- Usage/plan dashboard

### Phase 6: Reliability & Security
- Rate limit, input validation hardening
- Async jobs for heavy analysis
- Error handling, retries, idempotency

### Phase 7: Ship
- CI pipeline (lint/test/build)
- Production compose/k8s manifests
- README + setup guide + troubleshooting

## Commit Policy
- Commit after every finished micro-milestone.
- Conventional commits only.

## First 15 Micro-Milestones
1. Create monorepo skeleton
2. Add backend pyproject + lock
3. Add frontend package scaffolding
4. Docker compose postgres/redis
5. FastAPI app start + health endpoint
6. SQLAlchemy base + DB session wiring
7. Alembic init + first migration
8. User model + plan enum
9. Auth register endpoint + tests
10. Auth login/refresh + tests
11. Resume model + CRUD APIs
12. JD model + CRUD APIs
13. LangChain match chain v1
14. Match result persistence
15. Basic Next.js auth + dashboard shell

## Verification Gate per milestone
- Automated tests for touched area pass
- Manual sanity check documented
- Docs updated
- Commit completed
