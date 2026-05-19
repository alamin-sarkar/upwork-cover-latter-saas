# AGENTS.md — Execution Protocol

## Objective
Deliver a top-notch, production-ready Interview Copilot SaaS end-to-end, incrementally.

## Hard Rules
1. Never do too much in one run (respect execution/time limits).
2. Complete exactly one scoped milestone per run.
3. Every run must end with:
   - passing tests for touched scope,
   - updated docs/changelog,
   - a git commit.
4. No fake implementations, no dead code, no TODO placeholders for core paths.
5. Keep application_app untouched (critical external system rule).

## Architecture Targets
- FE: Next.js + TypeScript + React
- BE: FastAPI + PostgreSQL
- AI: LangChain + LangGraph
- Async: Redis + Celery
- Observability: structured logs + health checks

## Work Cadence
- Break work into micro-milestones (60–180 min each)
- Validate before commit
- Prefer reversible changes

## Definition of Done (per milestone)
- Tests added/updated and passing
- Lint/type checks pass for affected modules
- API contracts documented if changed
- Commit message follows conventional commits
