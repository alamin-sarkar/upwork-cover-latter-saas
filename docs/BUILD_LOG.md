# Build Log

## 2026-05-19 11:02 (Asia/Dhaka)
- Completed micro-milestone: Monorepo skeleton setup.
- Created directories:
  - `apps/web`
  - `apps/api`
  - `packages/ai-workflows`
  - `infra`
  - `.github/workflows`
- Added placeholder tracking files (`.gitkeep`) for clean Git structure.
- Validation:
  - Verified directory structure exists.

## 2026-05-19 11:08 (Asia/Dhaka)
- Completed micro-milestone: FastAPI bootstrap + PostgreSQL config scaffold + health endpoint + Alembic baseline.
- Added under `apps/api`:
  - `pyproject.toml` (FastAPI, SQLAlchemy, Alembic, psycopg, pytest)
  - `.env.example` (PostgreSQL connection scaffold)
  - `app/core/config.py`, `app/core/db.py`, `app/main.py`
  - `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`, `alembic/versions/0001_baseline.py`
  - `tests/test_health.py`, `README.md`
- Validation:
  - `pytest -q` => `1 passed`

## 2026-05-19 11:14 (Asia/Dhaka)
- Completed micro-milestone: Next.js + TypeScript + base auth shell scaffold.
- Added under `apps/web`:
  - Next.js app bootstrap (App Router, TypeScript, Tailwind, ESLint)
  - Home page with Login/Register navigation
  - `src/app/login/page.tsx`
  - `src/app/register/page.tsx`
- Validation:
  - `npm run lint` => pass
  - `npm run build` => pass
- Next step:
  - Implement JWT auth endpoints and user/plan schema in backend.

## 2026-05-19 11:52 (Asia/Dhaka)
- Completed planning/doc-alignment milestone for product repositioning.
- Reframed the project from interview copilot direction to **Upwork Cover Letter AI SaaS**.
- Updated root planning/agent files:
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `MEMORY.md`
  - `docs/MASTER_PLAN.md`
  - `docs/plans/2026-05-19-upwork-cover-letter-saas-implementation-plan.md`
- Established domain scope for:
  - structured user profile sections
  - writing guidelines and sample letters
  - job-post analysis
  - multi-structure cover-letter generation
  - feedback memory and history
  - MCP integration
- Validation:
  - reviewed repository state
  - ensured doc changes are additive and do not disturb in-progress auth backend files
- Next step:
  - Finish backend auth milestone already in progress before building profile/settings domain.

## 2026-05-19 13:30 (Asia/Dhaka)
- Completed micro-milestone: backend auth foundation.
- Added backend auth domain under `apps/api`:
  - `app/api/routes/auth.py` for register, login, refresh, and current-user endpoints
  - `app/core/security.py` for password hashing and JWT issuance/verification
  - `app/core/deps.py` for DB session and bearer-token current-user resolution
  - `app/models/user.py` and `app/models/__init__.py` for user, role, and plan persistence
  - `app/schemas/auth.py`, `app/schemas/user.py`, and package exports for request/response contracts
- Updated bootstrap files:
  - `app/main.py` to mount auth routes
  - `app/core/config.py` and `.env.example` for JWT settings
  - `alembic/versions/0001_baseline.py` to create the users table
  - `pyproject.toml` for auth-related dependencies
  - `apps/api/README.md` with auth endpoint and run/test instructions
- Added TDD coverage:
  - `tests/test_auth.py` for register, duplicate email rejection, login, invalid password rejection, `/me`, refresh, and refresh token misuse
- Validation:
  - `.venv/bin/python -m pytest -q` => `8 passed`
- Next step:
  - Build authenticated profile/settings module on top of this auth base.

## 2026-05-19 13:50 (Asia/Dhaka)
- Completed micro-milestone: profile settings backend foundation (profile + skills).
- Added backend profile domain under `apps/api`:
  - `app/models/profile.py` with `Profile` and `ProfileSkill` models
  - `app/schemas/profile.py` for profile and skill request/response contracts
  - `app/api/routes/profile.py` with authenticated endpoints:
    - `GET /api/v1/profile`
    - `PUT /api/v1/profile`
    - `GET /api/v1/profile/skills`
    - `POST /api/v1/profile/skills`
    - `DELETE /api/v1/profile/skills/{skill_id}`
- Integrated profile router into API bootstrap:
  - `app/api/routes/__init__.py`
  - `app/api/__init__.py`
  - `app/main.py`
- Added migration:
  - `alembic/versions/0002_profile_and_skills.py`
- Added TDD coverage:
  - `tests/test_profile.py` for auto-profile creation, profile update, skill add/list, duplicate-skill rejection
- Validation:
  - `.venv/bin/python -m pytest -q` => `12 passed`
- Next step:
  - Extend settings domain with projects/professional-life/custom sections and CRUD APIs.

## 2026-05-19 14:05 (Asia/Dhaka)
- Completed micro-milestone: projects + professional-life + custom sections CRUD APIs.
- Extended profile settings backend under `apps/api`:
  - `app/models/profile.py` with new entities:
    - `ProfileProject`
    - `ProfileProfessionalLife`
    - `ProfileCustomSection`
  - `app/schemas/profile.py` with create/read schemas for all three sections
  - `app/api/routes/profile.py` with authenticated endpoints:
    - Projects: `GET/POST/DELETE /api/v1/profile/projects`
    - Professional life: `GET/POST/DELETE /api/v1/profile/professional-life`
    - Custom sections: `GET/POST/DELETE /api/v1/profile/custom-sections`
- Export updates:
  - `app/models/__init__.py`
  - `app/schemas/__init__.py`
- Added migration:
  - `alembic/versions/0003_profile_projects_professional_custom_sections.py`
- Expanded API tests:
  - `tests/test_profile.py` now covers CRUD flow for projects, professional-life entries, and custom sections
- Validation:
  - `.venv/bin/python -m pytest -q` => `15 passed`
- Next step:
  - Add update endpoints for these sections and start guideline/sample library module.

## 2026-05-19 14:54 (Asia/Dhaka)
- Completed micro-milestone: update endpoints (PATCH) + guideline/sample library module.
- Added PATCH endpoints for mutable profile sections:
  - `PATCH /api/v1/profile/projects/{project_id}`
  - `PATCH /api/v1/profile/professional-life/{entry_id}`
  - `PATCH /api/v1/profile/custom-sections/{section_id}`
- Added new guideline + sample library module:
  - `GET/POST/PATCH/DELETE /api/v1/profile/guidelines`
  - `GET/POST/PATCH/DELETE /api/v1/profile/samples`
- Extended profile models and schemas with guideline/sample entities and update DTOs.
- Added migration:
  - `alembic/versions/0004_profile_guidelines_samples.py`
- Expanded tests for PATCH flows and guideline/sample CRUD/PATCH.
- Validation:
  - `.venv/bin/python -m pytest -q` => `17 passed`
- Next step:
  - Start cover-letter generation engine scaffold (job ingestion + prompt orchestration + history linkage).

## 2026-05-19 15:05 (Asia/Dhaka)
- Completed micro-milestone: cover-letter generation engine scaffold.
- Added new cover-letter domain:
  - `app/models/cover_letter.py` with:
    - `CoverLetterJobPost`
    - `CoverLetterGeneration`
- Added cover-letter API routes:
  - `POST /api/v1/cover-letter/job-posts`
  - `GET /api/v1/cover-letter/job-posts`
  - `POST /api/v1/cover-letter/generate`
  - `GET /api/v1/cover-letter/history`
- Added schema contracts:
  - `app/schemas/cover_letter.py`
- Wired router into API bootstrap:
  - `app/api/routes/__init__.py`
  - `app/api/__init__.py`
  - `app/main.py`
- Added migration:
  - `alembic/versions/0005_cover_letter_engine_scaffold.py`
- Added scaffold test coverage:
  - `tests/test_cover_letter.py` (job post create → generate 3 variants → history listing)
- Validation:
  - `.venv/bin/python -m pytest -q` => `18 passed`
- Next step:
  - feedback-memory loop (user feedback on generated letter + apply preference signals in next generations).

## 2026-05-19 15:15 (Asia/Dhaka)
- Completed micro-milestone: feedback-memory loop.
- Added feedback persistence for cover-letter generations:
  - new model: `CoverLetterFeedback`
  - new migration: `alembic/versions/0006_cover_letter_feedback_memory.py`
- Added new APIs:
  - `POST /api/v1/cover-letter/feedback`
  - `GET /api/v1/cover-letter/memory-signal`
- Updated generation logic to read recent feedback trend and include preference guidance in analysis summary.
- Extended schemas for feedback and memory-signal contracts.
- Added test coverage:
  - `test_feedback_memory_loop_applies_signal` in `tests/test_cover_letter.py`
- Validation:
  - `.venv/bin/python -m pytest -q` => `19 passed`
- Next step:
  - LangChain/LangGraph-based prompt orchestration module (replace scaffold text with graph-driven generation).

## 2026-05-19 15:28 (Asia/Dhaka)
- Completed micro-milestone: LangChain/LangGraph orchestration scaffold.
- Added orchestration service:
  - `app/services/cover_letter_graph.py`
  - Introduced graph-driven generation pipeline with fallback execution path.
- Updated generation API to use orchestration service instead of inline variant text assembly.
- Added dependencies in `apps/api/pyproject.toml`:
  - `langchain`
  - `langgraph`
- Expanded tests:
  - `test_langgraph_orchestration_path_in_generation` in `tests/test_cover_letter.py`
- Validation:
  - `.venv/bin/python -m pytest -q` => `20 passed`
- Next step:
  - integrate real LLM provider node (prompt templates + structured output parsing per structure type).

## 2026-05-19 15:38 (Asia/Dhaka)
- Completed micro-milestone: real LLM node integration scaffold (provider config + prompt templates + structure parser path).
- Extended provider configuration:
  - `app/core/config.py`
  - `.env.example`
  - Added: `LLM_PROVIDER`, `LLM_MODEL`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`
- Upgraded orchestration service:
  - `app/services/cover_letter_graph.py`
  - Added prompt-template builder node
  - Added provider invocation node scaffold
  - Added JSON structured output parser node
  - Added structure-wise prompt instructions (`direct-value`, `problem-solution`, `story-proof`)
- Expanded tests:
  - `test_structure_wise_output_parser_behavior` in `tests/test_cover_letter.py`
- Validation:
  - `.venv/bin/python -m pytest -q` => `21 passed`
- Next step:
  - wire actual provider clients (OpenRouter/Groq/Gemini) with fallback chain + timeout/retry policy.

## 2026-05-19 15:48 (Asia/Dhaka)
- Completed micro-milestone: actual provider client wiring scaffold with fallback chain + timeout/retry + error-safe contract.
- Updated `app/services/cover_letter_graph.py`:
  - Added provider candidate chain logic (`LLM_PROVIDER` first, then OpenRouter/Groq/Gemini, then mock).
  - Added HTTP client invocation via `httpx` for OpenAI-compatible chat endpoints.
  - Added retry policy (3 attempts, incremental backoff) and timeout control.
  - Added error aggregation and graceful fallback JSON contract when providers fail.
- Added regression test:
  - `test_provider_fallback_error_safe_contract` in `tests/test_cover_letter.py`.
- Validation:
  - `.venv/bin/python -m pytest -q` => `22 passed`
- Next step:
  - add provider-specific model mapping + JSON schema enforcement and telemetry for fallback reason tracking.
