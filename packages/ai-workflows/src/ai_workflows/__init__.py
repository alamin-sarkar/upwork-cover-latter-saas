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

__all__ = [
    "JOB_ANALYSIS_PROMPT_VERSION",
    "JobAnalysis",
    "build_job_analysis_graph",
    "build_job_analysis_prompt",
]
