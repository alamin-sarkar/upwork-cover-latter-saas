from __future__ import annotations

import json
import time
from typing import TypedDict

import httpx

from app.core.config import settings

try:
    from langgraph.graph import END, StateGraph
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
    prompt_text: str
    llm_raw_output: str


def _get_structure_prompt(structure: str) -> str:
    prompts = {
        "direct-value": "Write a concise value-first cover letter: opening value, relevant skill match, concrete delivery plan.",
        "problem-solution": "Write problem-solution style: restate core need, solution approach, implementation confidence.",
        "story-proof": "Write a short proof-based story: similar work, measurable result, clear next step.",
    }
    return prompts.get(structure, prompts["direct-value"])


def _build_prompt(state: CoverLetterState) -> CoverLetterState:
    template = (
        "You are generating an Upwork cover letter.\n"
        "Return strict JSON with keys: analysis_summary, draft_text.\n"
        "Job title: {job_title}\n"
        "Job details: {raw_text}\n"
        "Candidate headline: {headline}\n"
        "Guidelines: {guideline_text}\n"
        "Tone hint: {tone_hint}\n"
        "Preference note: {preference_note}\n"
        "Structure instruction: {structure_prompt}\n"
    )
    state["prompt_text"] = template.format(
        job_title=state["job_title"],
        raw_text=state["raw_text"],
        headline=state["headline"],
        guideline_text=state["guideline_text"],
        tone_hint=state["tone_hint"],
        preference_note=state["preference_note"],
        structure_prompt=_get_structure_prompt(state["structure"]),
    )
    return state


def _provider_candidates() -> list[tuple[str, str | None, str, str]]:
    # priority: requested provider first, then fallback chain
    configured = (settings.LLM_PROVIDER or "mock").lower()
    base = [
        ("openrouter", settings.OPENROUTER_API_KEY, "https://openrouter.ai/api/v1/chat/completions", settings.LLM_MODEL),
        ("groq", settings.GROQ_API_KEY, "https://api.groq.com/openai/v1/chat/completions", settings.LLM_MODEL),
        ("gemini", settings.GEMINI_API_KEY, "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", settings.LLM_MODEL),
    ]
    order = [configured] + [x[0] for x in base if x[0] != configured]
    by_name = {x[0]: x for x in base}
    out = [by_name[n] for n in order if n in by_name]
    out.append(("mock", None, "", "mock-cover-letter-v1"))
    return out


def _call_with_retry(provider: str, api_key: str, url: str, model: str, prompt_text: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Output must be valid JSON only."},
            {"role": "user", "content": prompt_text},
        ],
        "temperature": 0.3,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    last_err = "unknown"
    for attempt in range(1, 4):
        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.post(url, headers=headers, json=payload)
            if resp.status_code >= 500:
                raise RuntimeError(f"server error {resp.status_code}")
            resp.raise_for_status()
            body = resp.json()
            return body["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            last_err = f"{provider} attempt {attempt}: {exc}"
            time.sleep(0.5 * attempt)
    raise RuntimeError(last_err)


def _invoke_llm_node(state: CoverLetterState) -> CoverLetterState:
    errors: list[str] = []
    for provider, key, url, model in _provider_candidates():
        if provider == "mock":
            break
        if not key:
            errors.append(f"{provider}: missing api key")
            continue
        try:
            state["llm_raw_output"] = _call_with_retry(provider, key, url, model, state["prompt_text"])
            return state
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))
            continue

    fallback_json = {
        "analysis_summary": (
            f"Analyze: {state['job_title']}. Priorities: {state['guideline_text']}. "
            f"Tone hint: {state['tone_hint']}. {state['preference_note']}"
        ).strip(),
        "draft_text": _fallback_draft_by_structure(state),
        "meta": {"fallback": True, "errors": errors[:3]},
    }
    state["llm_raw_output"] = json.dumps(fallback_json)
    return state


def _parse_output(state: CoverLetterState) -> CoverLetterState:
    try:
        payload = json.loads(state["llm_raw_output"])
    except Exception:
        payload = {"analysis_summary": f"Analyze: {state['job_title']}", "draft_text": _fallback_draft_by_structure(state)}

    state["analysis_summary"] = str(payload.get("analysis_summary") or "").strip() or f"Analyze: {state['job_title']}"
    state["draft_text"] = str(payload.get("draft_text") or "").strip() or _fallback_draft_by_structure(state)
    return state


def _fallback_draft_by_structure(state: CoverLetterState) -> str:
    if state["structure"] == "direct-value":
        return f"Hi, I noticed your {state['job_title']} project. I'm {state['headline']} and can deliver quickly with clear milestones."
    if state["structure"] == "problem-solution":
        return f"Your requirement suggests immediate execution needs. As {state['headline']}, I can design and ship a reliable solution end-to-end."
    return f"I recently completed a similar project with measurable impact. For your {state['job_title']}, I can provide the same outcome with transparent communication."


def _run_fallback(state: CoverLetterState) -> CoverLetterState:
    state = _build_prompt(state)
    state = _invoke_llm_node(state)
    state = _parse_output(state)
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
        "prompt_text": "",
        "llm_raw_output": "",
    }

    if StateGraph is None:
        result = _run_fallback(initial_state)
    else:
        graph = StateGraph(CoverLetterState)
        graph.add_node("build_prompt", _build_prompt)
        graph.add_node("invoke_llm", _invoke_llm_node)
        graph.add_node("parse_output", _parse_output)
        graph.set_entry_point("build_prompt")
        graph.add_edge("build_prompt", "invoke_llm")
        graph.add_edge("invoke_llm", "parse_output")
        graph.add_edge("parse_output", END)
        compiled = graph.compile()
        result = compiled.invoke(initial_state)

    return {"analysis_summary": result["analysis_summary"], "draft_text": result["draft_text"]}
