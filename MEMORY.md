# Project Memory

Stable project context and working conventions for future implementation runs.

## Product Identity
- Working product name: Upwork Cover Letter AI SaaS
- Purpose: analyze Upwork job posts and generate personalized, high-conversion cover letters using stored user profile data, writing rules, examples, and memory from prior feedback.

## Delivery Strategy
- Build in small phases over multiple days; do not attempt the whole platform in one run.
- One micro-milestone per run.
- Preserve usage budget by favoring narrow, testable increments.
- After each completed milestone: tests, docs/build log update, git review, commit, and push when remote is available.

## Documentation Rules
- Keep root `README.md`, `AGENTS.md`, and `CLAUDE.md` aligned with the active product direction.
- Update `docs/BUILD_LOG.md` after each completed milestone.
- Keep roadmap changes reflected in `docs/MASTER_PLAN.md`.
- Save phase-level execution plans under `docs/plans/`.

## Domain Rules
- User profile is multi-section and extensible: skills, projects, professional life, niche/domain preferences, writing guidance, examples, and future custom sections.
- Every cover-letter generation should be backed by explicit job analysis plus evidence matching from user data.
- System should support multiple output structures for cover letters, not a single generic format.
- Feedback memory must influence future generations.
- History must store raw inputs, analyzed results, generated drafts, edits, and feedback metadata.
- MCP support is required so external AI tools/platforms can connect to user profile, guidelines, samples, and generation workflows.

## Technical Preferences
- Backend: FastAPI
- Frontend: Next.js
- Database: PostgreSQL
- AI orchestration: LangChain + LangGraph
- RAG: optional, only when needed for retrieval over user examples/guidelines/history
- Prefer PostgreSQL + pgvector before introducing more infrastructure
- In `apps/web`, `tsconfig.json` includes `.next/types`, so run `next build` before standalone `npm run typecheck` when verifying route changes.
- API runtime now treats `X-Request-ID` as the canonical trace header and exposes `/health/ready` plus `/admin/diagnostics` for operational checks.
- Plan-based daily limits are enforced on job analysis and generation surfaces; Redis is the primary backend with in-memory fallback for local/test execution.
- Celery workers start from `app.worker.celery_app`, and deployment verification should include the diagnostics endpoint plus worker visibility.
- API startup imports `app.core.workspace_imports` first so local monorepo runs can resolve `packages/ai-workflows/src` even when `ai-workflows` was not reinstalled in the active virtual environment.

## Safety Rules
- Do not touch `application_app`.
- Do not commit `.venv`, `.next`, caches, or generated artifacts.
- Review `git status --short` before each commit.
