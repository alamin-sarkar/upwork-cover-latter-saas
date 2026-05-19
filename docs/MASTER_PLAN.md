# Upwork Cover Letter AI SaaS — Master Plan

## Goal
Build and ship a production-grade AI SaaS that turns a target Upwork job post into multiple personalized cover-letter drafts using structured user profile data, example letters, writing guidelines, and feedback memory.

## Success Criteria
- A user can manage a rich profile once and reuse it repeatedly
- A user can paste a job post and receive:
  - structured job analysis,
  - match reasoning against their own profile,
  - multiple cover-letter structures,
  - improvement notes and risk flags
- User feedback on generated letters improves future generations
- Full history, auditing, and user management exist
- MCP integration allows external AI tools to access controlled profile/guideline/sample resources

## Monorepo Layout
- `apps/web` — Next.js frontend
- `apps/api` — FastAPI backend
- `packages/ai-workflows` — LangGraph graphs, prompts, evaluators, schemas
- `infra/` — docker, deployment, CI/CD, environment templates
- `docs/` — architecture, ADRs, API contracts, runbooks, phased plans
- `MEMORY.md` — stable project conventions and direction

## System Modules
### 1. Identity & Access
- registration/login/refresh/me
- roles and subscription plans
- session tracking and audit events

### 2. User Profile System
- basic identity/profile meta
- skills
- projects / case studies
- professional life / work history
- niche/domain preferences
- tools/stack familiarity
- custom sections for future extensibility

### 3. Writing Assets
- cover-letter guidelines
- reusable intros/CTAs/hooks
- tone presets
- user-provided sample cover letters
- tagged winning examples and anti-pattern examples

### 4. Job Intake & Analysis
- paste raw Upwork job post
- structured extraction:
  - title
  - scope
  - deliverables
  - required skills
  - budget clues
  - urgency
  - communication tone
  - risk flags
- fit scoring against profile evidence

### 5. Generation Engine
- LangGraph workflow:
  - normalize input
  - analyze job
  - retrieve profile evidence
  - retrieve relevant guidelines/examples
  - draft multiple variants
  - self-check against constraints
  - return structured output
- supported structures:
  - concise/high-impact
  - problem-solution
  - credibility-first
  - portfolio-first
  - consultative/discovery-first

### 6. Feedback Memory
- user rating
- edited final version
- accepted/rejected sections
- client response outcome if available
- learned preferences and recurring corrections

### 7. History & Workspace
- generation history
- compare versions
- favorite templates
- re-run with new strategy
- search old letters

### 8. MCP Integration Layer
- expose profile/guideline/sample/history resources safely
- allow external AI platforms to request generation with scoped permissions
- provide tool/resource contracts for portable automation

### 9. Reliability & Admin
- observability
- rate limiting
- usage quotas
- background jobs
- admin diagnostics
- prompt/version auditability

## Phase Plan

### Phase 0 — Product Direction & Guardrails
- align project docs to product scope
- create execution protocol and memory docs
- define phases and milestone order

### Phase 1 — Core Platform Foundation
- FastAPI app factory, config, DB session, health endpoints
- Next.js app shell
- docker compose baseline
- repo hygiene and CI foundations

### Phase 2 — Authentication & User Management
- user model and plan enum
- register/login/refresh/me
- password hashing and JWT
- auth tests and migrations

### Phase 3 — Profile Settings Domain
- profile aggregate and section tables
- CRUD APIs for skills, projects, professional life, niches, custom sections
- settings UI with sectioned forms
- tests for validation and ownership rules

### Phase 4 — Writing Guidance & Examples
- guideline entities and versioning
- sample cover-letter entities with tags/outcomes
- retrieval strategy for generation-time context
- UI for managing guidelines/examples

### Phase 5 — Job Post Intake & Analysis
- raw post ingestion endpoint
- structured extraction pipeline
- fit scoring and evidence matching
- storage for job analysis snapshots
- UI for paste/analyze flow

### Phase 6 — Cover Letter Generation Engine
- LangChain prompt layer
- LangGraph orchestration
- multiple letter structures
- output schema validation and guardrails
- regenerate with strategy controls

### Phase 7 — Feedback Memory & Continuous Improvement
- rating/edit/final-selection APIs
- learned preference extraction
- memory retrieval in later generations
- outcome tracking and analytics primitives

### Phase 8 — History, Search, and Workspace UX
- searchable generation history
- compare outputs
- saved favorites and template reuse
- dashboard metrics

### Phase 9 — MCP Integration
- MCP resources/tools for profile, guidelines, samples, generation
- permission/scoping model
- integration docs and verification scripts

### Phase 10 — Production Hardening
- Celery/Redis async workflows
- rate limits and quotas
- logs, traces, alerts
- CI/CD and deployment docs
- security review and backup strategy

## First 20 Micro-Milestones
1. Align project docs to new product direction
2. Finish backend auth scaffolding already in progress
3. Add auth schemas and tests
4. Add auth migrations and validation gates
5. Create profile aggregate models
6. Create skills/projects/professional-life models
7. Add profile CRUD APIs
8. Build settings UI shell
9. Add guideline models and CRUD APIs
10. Add sample letter models and CRUD APIs
11. Build writing-assets settings screens
12. Add job-post intake API
13. Add structured job-analysis service
14. Persist job analysis results
15. Design generation prompt contracts and output schema
16. Build LangGraph v1 generation workflow
17. Add multiple cover-letter strategy variants
18. Add feedback capture APIs and memory rules
19. Build history/search UI and APIs
20. Add MCP resource/tool endpoints

## Technical Decisions
- PostgreSQL is the source of truth
- pgvector is the default retrieval layer for embeddings/similarity
- RAG is optional and should only be added where retrieval quality benefits are clear
- Prompt templates and output schemas should be versioned
- Every generation run should store enough metadata for later debugging and evaluation

## Verification Gate per Milestone
- Automated tests for touched scope pass
- Manual sanity-check documented in `docs/BUILD_LOG.md`
- Docs updated
- `git status --short` reviewed for artifact leaks
- Commit completed
