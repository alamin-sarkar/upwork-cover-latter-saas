# AGENTS.md — Execution Protocol

## Objective
Build a production-grade Upwork Cover Letter AI SaaS incrementally, with each run completing one safe, reviewable micro-milestone.

## Resume protocol
When the user asks to "continue", "start the next phase", or anything similar **without naming a phase**: open `docs/PHASE_TRACKER.md` first. It owns the "Current pointer" line, per-phase scope, and acceptance criteria. After shipping a phase, update the checkbox + pointer there, append to `docs/BUILD_LOG.md`, and commit. Never skip phases.

## Product Scope
The product analyzes an Upwork job post, matches it with a user's structured profile and memory, and generates multiple personalized cover-letter variants plus guidance.

## Hard Rules
1. Never do too much in one run.
2. Complete exactly one scoped milestone per run.
3. Always preserve existing working functionality.
4. End every milestone with:
   - passing tests for touched scope,
   - updated docs/build log,
   - clean `git status --short` review,
   - a focused git commit.
5. Do not touch `application_app`.
6. Do not replace production-grade logic with mock placeholders on core paths.
7. Prefer additive, reversible changes over sweeping refactors.

## Architecture Targets
- FE: Next.js + TypeScript + React
- BE: FastAPI + PostgreSQL
- AI: LangChain + LangGraph
- Retrieval/Memory: PostgreSQL + pgvector, optional RAG only where it adds measurable value
- Async: Redis + Celery
- Integration: MCP-compatible endpoints/tools for external AI platforms
- Observability: structured logs, health checks, request tracing hooks

## Work Cadence
- Break work into micro-milestones sized for 60–180 minutes
- Keep milestone scope narrow enough to test thoroughly
- Validate before commit
- Update `MEMORY.md` when a stable project convention changes
- Record completed milestone notes in `docs/BUILD_LOG.md`

## Definition of Done (per milestone)
- Tests added/updated for the touched area and passing
- Lint/type checks pass for touched modules
- Docs updated if contracts, flows, or behavior changed
- No accidental artifacts staged (`.venv`, `.next`, caches, build output)
- Commit message uses conventional commits

## Current Preferred Build Order
1. Backend auth completion
2. User profile domain (skills, projects, professional summary, writing settings)
3. Cover-letter guideline and sample library
4. Job post ingestion + analysis pipeline
5. Cover-letter generation graph with multiple structures
6. History, feedback memory, and iterative improvement loop
7. Frontend dashboard and workflow screens
8. MCP integration surface
9. Reliability, billing/usage limits, admin tools, deployment hardening
