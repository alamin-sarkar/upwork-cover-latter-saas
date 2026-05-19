# Upwork Cover Letter AI SaaS

Production-grade AI SaaS for analyzing Upwork job posts and generating high-quality, personalized cover letters using each user's profile, work history, project evidence, writing preferences, and feedback memory.

## Product Vision
This platform helps freelancers and agencies stop writing cover letters from scratch. A user maintains a structured profile once, stores winning examples and writing rules, then pastes a target Upwork job post. The AI analyzes the post, matches it against the user's data, and produces multiple tailored cover-letter variations with rationale, confidence notes, and reusable suggestions.

## Core Value
- Upwork job post → structured analysis
- User profile + project proof + writing guidelines → personalized generation
- Multiple cover-letter structures, not one generic draft
- Feedback memory so later letters improve from earlier accept/reject/user edits
- Full history and audit trail for every generated result
- MCP-ready integration layer so external AI tools can sync profile, guidelines, and samples

## Planned Stack
- Frontend: Next.js (App Router), TypeScript, Tailwind, TanStack Query, Zustand
- Backend: FastAPI, SQLAlchemy 2, Pydantic v2, Alembic, PostgreSQL
- AI: LangChain, LangGraph, provider abstraction, prompt/version management
- Retrieval/Memory: PostgreSQL + pgvector, optional Redis cache, selective RAG
- Async: Celery + Redis
- Auth: JWT access/refresh, role-based user management
- Integrations: MCP server/client surface for external AI platforms
- Observability: structured logs, tracing hooks, health checks, admin diagnostics

## Monorepo Layout
- `apps/web` — Next.js frontend
- `apps/api` — FastAPI backend
- `packages/ai-workflows` — prompts, graphs, evaluators, shared schemas
- `infra/` — docker, deployment, CI assets
- `docs/` — architecture, plans, runbooks, product docs
- `MEMORY.md` — project memory and working conventions for future runs

## Current Status
- ✅ Monorepo skeleton exists
- ✅ FastAPI bootstrap and health endpoint exist
- ✅ Next.js auth shell scaffold exists
- ⏳ Auth backend is in progress
- ✅ Product direction updated for Upwork Cover Letter AI SaaS
- ✅ Root planning, agent instructions, and memory docs prepared for phased delivery

## Delivery Principles
- Small, reversible milestones
- One meaningful scope at a time
- Tests + docs + verification before each milestone is considered done
- No fake AI paths or placeholder core behavior
- Preserve user usage budget by delivering incrementally over multiple days

## Immediate Next Milestone
Complete backend authentication (register, login, refresh, me, migration, tests) so later profile, history, and AI features can attach to real users.
