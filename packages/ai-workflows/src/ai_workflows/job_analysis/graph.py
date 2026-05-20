from collections.abc import Awaitable, Callable
from typing import TypedDict

from ai_workflows.job_analysis.schemas import JobAnalysis
from langgraph.graph import END, START, StateGraph

Analyzer = Callable[[str], Awaitable[JobAnalysis]]


class JobAnalysisState(TypedDict):
    raw_job_text: str
    analysis: JobAnalysis | None


def build_job_analysis_graph(analyzer: Analyzer):
    graph = StateGraph(JobAnalysisState)

    async def analyze_job_post(state: JobAnalysisState) -> dict[str, JobAnalysis]:
        return {"analysis": await analyzer(state["raw_job_text"])}

    graph.add_node("analyze_job_post", analyze_job_post)
    graph.add_edge(START, "analyze_job_post")
    graph.add_edge("analyze_job_post", END)
    return graph.compile()
