from __future__ import annotations

from typing import TypedDict

try:
    from langgraph.graph import StateGraph, END
except Exception:  # pragma: no cover
    StateGraph = None
    END = None


class CoverLetterState(TypedDict):
    job_title: str
    raw_text: str
    headline: str
    guideline_text: str
    tone_hint: str
    preference_note: str
    structure: str
    analysis_summary: str
    draft_text: str


def _analyze_job(state: CoverLetterState) -> CoverLetterState:
    state["analysis_summary"] = (
        f"Analyze: {state['job_title']}. Priorities: {state['guideline_text']}. "
        f"Tone hint: {state['tone_hint']}. {state['preference_note']}"
    ).strip()
    return state


def _compose_draft(state: CoverLetterState) -> CoverLetterState:
    if state["structure"] == "direct-value":
        draft = f"Hi, I noticed your {state['job_title']} project. I'm {state['headline']} and can deliver quickly with clear milestones."
    elif state["structure"] == "problem-solution":
        draft = f"Your requirement suggests immediate execution needs. As {state['headline']}, I can design and ship a reliable solution end-to-end."
    else:
        draft = f"I recently completed a similar project with measurable impact. For your {state['job_title']}, I can provide the same outcome with transparent communication."
    state["draft_text"] = draft
    return state


def _run_fallback(state: CoverLetterState) -> CoverLetterState:
    state = _analyze_job(state)
    state = _compose_draft(state)
    return state


def run_cover_letter_graph(*, job_title: str, raw_text: str, headline: str, guideline_text: str, tone_hint: str, preference_note: str, structure: str) -> dict[str, str]:
    initial_state: CoverLetterState = {
        "job_title": job_title,
        "raw_text": raw_text,
        "headline": headline,
        "guideline_text": guideline_text,
        "tone_hint": tone_hint,
        "preference_note": preference_note,
        "structure": structure,
        "analysis_summary": "",
        "draft_text": "",
    }

    if StateGraph is None:
        result = _run_fallback(initial_state)
    else:
        graph = StateGraph(CoverLetterState)
        graph.add_node("analyze_job", _analyze_job)
        graph.add_node("compose_draft", _compose_draft)
        graph.set_entry_point("analyze_job")
        graph.add_edge("analyze_job", "compose_draft")
        graph.add_edge("compose_draft", END)
        compiled = graph.compile()
        result = compiled.invoke(initial_state)

    return {
        "analysis_summary": result["analysis_summary"],
        "draft_text": result["draft_text"],
    }
