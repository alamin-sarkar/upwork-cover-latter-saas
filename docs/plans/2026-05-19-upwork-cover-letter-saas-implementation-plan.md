# Upwork Cover Letter AI SaaS Implementation Plan

> **For Hermes:** Use `subagent-driven-development` after each milestone plan is approved. Do not attempt the whole product at once.

**Goal:** Build a fully professional SaaS that analyzes Upwork job posts and generates multiple personalized cover-letter variants from structured user profile data, writing guidelines, samples, and feedback memory.

**Architecture:** Monorepo with Next.js frontend, FastAPI backend, PostgreSQL as source of truth, LangChain/LangGraph for orchestration, and pgvector-backed retrieval for examples/guidelines/history when useful. The platform is delivered in small, testable phases so cost, context, and risk remain controlled.

**Tech Stack:** Next.js, TypeScript, Tailwind, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, pgvector, LangChain, LangGraph, Celery, Redis, JWT auth, MCP.

---

## Delivery Rules
- One micro-milestone per run
- Prefer 2–5 minute implementation steps inside each milestone
- No broad refactors unless forced by tests or design correctness
- Update `docs/BUILD_LOG.md` after each completed milestone
- Review `git status --short` before every commit
- Push after commit when remote URL is configured/confirmed

## Phase A — Foundation and Identity

### Milestone A1: Complete backend authentication
**Objective:** Finish the in-progress auth backend so later profile and AI data can be tied to real users.

**Files:**
- Modify: `apps/api/pyproject.toml`
- Modify/Create: `apps/api/app/models/*.py`
- Modify/Create: `apps/api/app/schemas/*.py`
- Modify/Create: `apps/api/app/api/routes/auth.py`
- Modify/Create: `apps/api/tests/test_auth*.py`
- Modify/Create: `apps/api/alembic/versions/*.py`

**Steps:**
1. Inspect existing auth-related uncommitted files.
2. Add/complete schemas for register, login, token refresh, and current user.
3. Wire auth routes into FastAPI app.
4. Add Alembic migration for users/plan enum.
5. Write auth tests.
6. Run pytest for auth scope.
7. Update `docs/BUILD_LOG.md`.
8. Review `git status --short`.
9. Commit.

**Verification:**
- `pytest -q` in `apps/api` passes for auth tests
- register/login/refresh/me endpoints work locally

### Milestone A2: Create frontend auth integration shell
**Objective:** Connect existing login/register screens to the real auth API.

**Files:**
- Modify: `apps/web/src/app/login/page.tsx`
- Modify: `apps/web/src/app/register/page.tsx`
- Create: `apps/web/src/lib/api-client.ts`
- Create: `apps/web/src/lib/auth-store.ts`
- Create/Modify: `apps/web/src/middleware.ts` or route guard files as needed
- Test: `apps/web` unit/integration tests for auth flow

**Verification:**
- login/register screens submit successfully against API
- lint/build pass

---

## Phase B — User Profile Settings Domain

### Milestone B1: Design profile schema
**Objective:** Establish the normalized data model for profile sections and extensibility.

**Core entities:**
- `profiles`
- `profile_skills`
- `profile_projects`
- `profile_experiences`
- `profile_niches`
- `profile_custom_sections`
- `profile_preferences`

**Key decisions:**
- Each section belongs to one user
- Sections are ordered and optionally embeddable
- Projects store evidence snippets, metrics, stack, role, links
- Preferences store tone, banned phrases, CTA style, length rules

### Milestone B2: Build profile CRUD APIs
**Objective:** Let users create/update/delete structured profile content safely.

**Verification:**
- ownership checks enforced
- validation errors handled cleanly
- tests cover unauthorized access and invalid payloads

### Milestone B3: Build settings UI
**Objective:** Provide a sectioned settings experience for skills, projects, professional life, and custom sections.

**UX requirements:**
- accordion/tab sections
- autosave or explicit save with draft state
- reorderable items
- evidence-first project editing
- future-safe extensibility for new section types

---

## Phase C — Writing Guidelines and Sample Library

### Milestone C1: Guideline management backend
**Objective:** Store how the user wants letters to be written.

**Guideline examples:**
- hook style
- response length target
- avoid generic phrases
- always mention relevant proof
- ask one smart question at the end
- never sound desperate

### Milestone C2: Sample cover-letter backend
**Objective:** Store user-provided samples with tags and outcomes.

**Sample metadata:**
- title
- source type
- niche
- outcome status
- liked/disliked sections
- notes

### Milestone C3: Settings UI for guidelines and samples
**Objective:** Make writing assets editable and searchable from the dashboard.

---

## Phase D — Job Analysis Engine

### Milestone D1: Raw job post ingestion
**Objective:** Accept pasted Upwork job descriptions and save immutable raw input.

### Milestone D2: Structured extraction service
**Objective:** Convert a raw job post into normalized fields.

**Extraction fields:**
- problem summary
- deliverables
- required skills
- optional skills
- domain
- urgency
- client tone
- red flags
- likely evaluation criteria

### Milestone D3: Profile-to-job fit reasoning
**Objective:** Match user evidence to extracted requirements.

**Output should include:**
- strongest matching skills
- most relevant projects
- missing requirements
- angle suggestions for the letter

---

## Phase E — Generation Workflow

### Milestone E1: Prompt and output contract design
**Objective:** Define versioned structured outputs before generating real drafts.

**Output contract:**
- job analysis summary
- matching evidence list
- 3–5 cover-letter variants
- per-variant strategy label
- improvement notes
- risk notes

### Milestone E2: LangGraph v1 generation workflow
**Objective:** Create the first working orchestration graph.

**Graph stages:**
1. validate inputs
2. fetch user profile
3. fetch relevant guidelines
4. fetch relevant samples/history
5. analyze job
6. match evidence
7. generate variants
8. self-check against rules
9. persist run record

### Milestone E3: Variant strategy set
**Objective:** Support different professional structures.

**Required first variant set:**
- concise value-first
- authority/proof-first
- problem-solution
- consultative

---

## Phase F — Memory and Learning Loop

### Milestone F1: Feedback capture
**Objective:** Save ratings, edits, accepted draft, and notes after each generation.

### Milestone F2: Learned preferences layer
**Objective:** Distill stable user preferences from repeated feedback.

**Examples:**
- prefers 120–150 words
- dislikes “I am excited to apply” openings
- prefers direct CTA
- wants project proof in second sentence

### Milestone F3: Memory-aware generation
**Objective:** Inject learned preferences into future generations safely.

**Guardrail:**
- learned memory must be overridable by current request

---

## Phase G — History, Search, and Workspace

### Milestone G1: Generation history backend
**Objective:** Store every run, variants, selected draft, and metadata.

### Milestone G2: Search/filter/compare UX
**Objective:** Let users review old cover letters and compare strategies.

### Milestone G3: Favorites and reusable templates
**Objective:** Turn successful drafts into reusable assets.

---

## Phase H — MCP and Integrations

### Milestone H1: MCP resource design
**Objective:** Decide what external AI platforms can read safely.

**Candidate resources:**
- profile summary
- skills/projects evidence
- writing guidelines
- sample letters
- learned preferences

### Milestone H2: MCP tool design
**Objective:** Expose controlled generation and retrieval actions.

**Candidate tools:**
- analyze_job_post
- get_profile_context
- get_cover_letter_guidelines
- generate_cover_letter_variants
- record_cover_letter_feedback

### Milestone H3: Authz and scoping
**Objective:** Ensure external access respects user permissions and consent.

---

## Phase I — Production Hardening

### Milestone I1: Async processing and queueing
### Milestone I2: Rate limits, quotas, and usage accounting
### Milestone I3: Structured logging and diagnostics
### Milestone I4: CI/CD, deployment, backup, and recovery docs

---

## Suggested File/Folder Expansion
- `apps/api/app/models/`
- `apps/api/app/schemas/`
- `apps/api/app/services/`
- `apps/api/app/repositories/`
- `apps/api/app/api/routes/`
- `apps/api/app/ai/`
- `apps/web/src/app/(dashboard)/`
- `apps/web/src/components/forms/`
- `apps/web/src/components/history/`
- `packages/ai-workflows/src/graphs/`
- `packages/ai-workflows/src/prompts/`
- `packages/ai-workflows/src/schemas/`
- `docs/plans/`
- `docs/adr/`

## Repo Hygiene Gates
1. Keep `.gitignore` updated before adding tooling.
2. Never stage `.venv/`, `.next/`, caches, or build artifacts.
3. Before commit run:
   - `git status --short`
   - `git diff --cached --name-only`
4. If artifacts leak into staging, clean with:
   - `git rm -r --cached <artifact_paths>`

## Recommended Next Action
Execute only **Milestone A1: Complete backend authentication** in the next implementation run. It is already partially scaffolded and unlocks the rest of the system.
