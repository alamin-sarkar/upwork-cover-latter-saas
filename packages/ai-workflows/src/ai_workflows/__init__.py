"""Shared AI workflow primitives (prompts, graphs, schemas).

Implemented incrementally across phases 6–8. This module is intentionally empty
in Phase 1.
"""

__version__ = "0.1.0"
from ai_workflows.job_analysis import (
    JOB_ANALYSIS_PROMPT_VERSION,
    JobAnalysis,
    build_job_analysis_graph,
    build_job_analysis_prompt,
)
from ai_workflows.generation import (
    COVER_LETTER_GENERATION_PROMPT_VERSION,
    COVER_LETTER_REVIEW_PROMPT_VERSION,
    CoverLetterReviewResult,
    CoverLetterStructure,
    DraftedCoverLetter,
    FinalCoverLetterVariant,
    build_cover_letter_draft_prompt,
    build_cover_letter_generation_graph,
    build_cover_letter_review_prompt,
)

__all__ = [
    "COVER_LETTER_GENERATION_PROMPT_VERSION",
    "COVER_LETTER_REVIEW_PROMPT_VERSION",
    "CoverLetterReviewResult",
    "CoverLetterStructure",
    "DraftedCoverLetter",
    "FinalCoverLetterVariant",
    "JOB_ANALYSIS_PROMPT_VERSION",
    "JobAnalysis",
    "build_cover_letter_draft_prompt",
    "build_cover_letter_generation_graph",
    "build_job_analysis_graph",
    "build_job_analysis_prompt",
    "build_cover_letter_review_prompt",
]
