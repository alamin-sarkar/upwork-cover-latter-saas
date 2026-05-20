from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypedDict

from ai_workflows.generation.schemas import (
    CoverLetterStructure,
    DraftedCoverLetter,
    FinalCoverLetterVariant,
)
from ai_workflows.job_analysis.schemas import JobAnalysis
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class CoverLetterGenerationState(TypedDict):
    raw_job_text: str | None
    analysis_snapshot_id: str | None
    analysis: JobAnalysis | None
    requested_structures: list[str] | None
    profile_context: str | None
    library_context: str | None
    feedback_memory_context: str | None
    drafted_variants: list[DraftedCoverLetter] | None
    final_variants: list[FinalCoverLetterVariant] | None


AnalyzeJob = Callable[[CoverLetterGenerationState], Awaitable[dict[str, object]]]
RetrieveProfile = Callable[[CoverLetterGenerationState], Awaitable[dict[str, str]]]
RetrieveLibrary = Callable[[CoverLetterGenerationState], Awaitable[dict[str, str]]]
RetrieveFeedbackMemory = Callable[[CoverLetterGenerationState], Awaitable[dict[str, str]]]
DraftVariants = Callable[[CoverLetterGenerationState], Awaitable[dict[str, list[DraftedCoverLetter]]]]
ReviewVariants = Callable[
    [CoverLetterGenerationState], Awaitable[dict[str, list[FinalCoverLetterVariant]]]
]


def build_cover_letter_generation_graph(
    *,
    analyze_job: AnalyzeJob,
    retrieve_profile: RetrieveProfile,
    retrieve_library: RetrieveLibrary,
    retrieve_feedback_memory: RetrieveFeedbackMemory,
    draft_variants: DraftVariants,
    review_variants: ReviewVariants,
):
    graph = StateGraph(CoverLetterGenerationState)

    async def normalize_input(
        state: CoverLetterGenerationState,
    ) -> dict[str, object]:
        requested = state.get("requested_structures") or []
        if not requested:
            resolved = [
                CoverLetterStructure.concise.value,
                CoverLetterStructure.problem_solution.value,
            ]
        else:
            deduped = list(dict.fromkeys(requested))
            resolved = deduped[:5]

        raw_job_text = state.get("raw_job_text")
        return {
            "raw_job_text": raw_job_text.strip() if raw_job_text else None,
            "requested_structures": resolved,
        }

    graph.add_node("normalize_input", normalize_input)
    graph.add_node("analyze_job", analyze_job)
    graph.add_node("retrieve_profile", retrieve_profile)
    graph.add_node("retrieve_library", retrieve_library)
    graph.add_node("retrieve_feedback_memory", retrieve_feedback_memory)
    graph.add_node("draft_variants", draft_variants)
    graph.add_node("review_variants", review_variants)

    graph.add_edge(START, "normalize_input")
    graph.add_edge("normalize_input", "analyze_job")
    graph.add_edge("analyze_job", "retrieve_profile")
    graph.add_edge("retrieve_profile", "retrieve_library")
    graph.add_edge("retrieve_library", "retrieve_feedback_memory")
    graph.add_edge("retrieve_feedback_memory", "draft_variants")
    graph.add_edge("draft_variants", "review_variants")
    graph.add_edge("review_variants", END)
    return graph.compile(checkpointer=InMemorySaver())
