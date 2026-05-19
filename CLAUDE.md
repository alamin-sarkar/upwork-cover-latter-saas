# CLAUDE.md — Project Build Contract

## Product
Upwork Cover Letter AI SaaS: structured freelancer profile + guideline memory + job-post analysis + multi-variant cover-letter generation + feedback-driven improvement.

## Non-Negotiables
- Production-minded code quality from day 1
- Security basics enabled early (auth, validation, rate limiting, secret hygiene)
- PostgreSQL-first schema design
- LangChain/LangGraph orchestration for AI flows
- Clear separation between frontend, backend, workflow engine, and integration layers
- Every AI output must be traceable to prompt version, user profile inputs, and job analysis context

## Core User Experience
1. User signs up and logs in
2. User configures profile sections:
   - skills
   - projects/case studies
   - professional background
   - niche/domain preferences
   - writing guidelines
   - sample cover letters
3. User submits a target Upwork job post
4. System analyzes the post and extracts key requirements, risks, tone, and likely client intent
5. AI matches the post against stored profile evidence and memory
6. System generates several cover-letter structures with reasoning and editable output
7. User edits, rates, and stores feedback
8. Future generations reuse that feedback memory automatically

## Tech Decisions
- Frontend: Next.js (App Router), TypeScript, React, Tailwind, TanStack Query
- Backend: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2
- DB: PostgreSQL
- Vector/Retrieval: pgvector first; external vector DB only if scaling demands it
- Queue: Celery + Redis
- Auth: JWT access/refresh, user/session audit events
- AI: LangChain + LangGraph + provider adapter layer
- Integrations: MCP server/client features for external AI tools
- Tests: Pytest for API/domain; frontend unit/e2e introduced by phase

## Domain Boundaries
- Identity: users, auth, sessions, roles, plans
- Profile: skills, projects, work history, niches, preferences
- Knowledge Assets: cover-letter guidelines, sample letters, prompt presets
- Generation: job analysis, evidence matching, draft generation, scoring
- Memory: user feedback, edits, accept/reject signals, quality preferences
- History: every generation run, inputs, outputs, edits, final selections
- Integration: MCP tools/resources for profile sync and draft generation

## Build Sequence
1. Repo bootstrap + baseline docs
2. FastAPI core + Postgres migrations
3. Auth + user/plan models
4. Profile settings domain
5. Guidelines/sample library domain
6. Job post ingestion and structured analysis
7. Cover-letter generation graph
8. Feedback memory and adaptive improvement
9. Next.js dashboard + workflow screens
10. MCP integration layer
11. Usage limits, observability, background jobs, deployment hardening

## Quality Gate
No milestone is complete without tests, docs, verification, and a focused commit.
