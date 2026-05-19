from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, TypedDict

import httpx
from pydantic import BaseModel, ValidationError

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
    telemetry: dict[str, Any]


class LLMOutputSchema(BaseModel):
    analysis_summary: str
    draft_text: str


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    env_key: str | None
    api_key: str | None
    url: str
    model: str


PROVIDER_MODEL_MAP: dict[str, str] = {
    "openrouter": "openai/gpt-4o-mini",
    "groq": "llama-3.1-70b-versatile",
    "gemini": "gemini-1.5-flash",
}


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


def _resolve_model(provider: str) -> str:
    configured = (settings.LLM_MODEL or "").strip()
    if configured and configured != "mock-cover-letter-v1":
        return configured
    return PROVIDER_MODEL_MAP.get(provider, "mock-cover-letter-v1")


def _provider_candidates() -> list[ProviderSpec]:
    configured = (settings.LLM_PROVIDER or "mock").lower()
    base = [
        ProviderSpec("openrouter", "OPENROUTER_API_KEY", settings.OPENROUTER_API_KEY, "https://openrouter.ai/api/v1/chat/completions", _resolve_model("openrouter")),
        ProviderSpec("groq", "GROQ_API_KEY", settings.GROQ_API_KEY, "https://api.groq.com/openai/v1/chat/completions", _resolve_model("groq")),
        ProviderSpec("gemini", "GEMINI_API_KEY", settings.GEMINI_API_KEY, "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", _resolve_model("gemini")),
    ]
    order = [configured] + [x.name for x in base if x.name != configured]
    by_name = {x.name: x for x in base}
    out = [by_name[n] for n in order if n in by_name]
    out.append(ProviderSpec("mock", None, None, "", "mock-cover-letter-v1"))
    return out


def _sanitize_error(err: Exception) -> str:
    msg = str(err)
    for key in [settings.OPENROUTER_API_KEY, settings.GROQ_API_KEY, settings.GEMINI_API_KEY]:
        if key:
            msg = msg.replace(key, "[REDACTED]")
    return msg


def _provider_health_check(spec: ProviderSpec) -> tuple[bool, str | None]:
    if spec.name == "mock":
        return True, None
    if not spec.api_key:
        return False, f"missing {spec.env_key}"
    if len(spec.api_key.strip()) < 12:
        return False, f"invalid {spec.env_key}"
    if not spec.url.startswith("https://"):
        return False, "invalid provider url"
    return True, None


def _call_with_retry(spec: ProviderSpec, prompt_text: str) -> str:
    payload = {
        "model": spec.model,
        "messages": [
            {"role": "system", "content": "Output must be valid JSON only."},
            {"role": "user", "content": prompt_text},
        ],
        "temperature": 0.3,
    }
    headers = {"Authorization": f"Bearer {spec.api_key}", "Content-Type": "application/json"}

    last_err = "unknown"
    for attempt in range(1, 4):
        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.post(spec.url, headers=headers, json=payload)
            if resp.status_code >= 500:
                raise RuntimeError(f"server error {resp.status_code}")
            resp.raise_for_status()
            body = resp.json()
            return body["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            last_err = f"{spec.name} attempt {attempt}: {_sanitize_error(exc)}"
            time.sleep(0.5 * attempt)
    raise RuntimeError(last_err)


def _invoke_llm_node(state: CoverLetterState) -> CoverLetterState:
    telemetry: dict[str, Any] = {"attempted": [], "failures": [], "selected_provider": "mock", "fallback": False}

    for spec in _provider_candidates():
        if spec.name == "mock":
            break

        telemetry["attempted"].append(spec.name)
        ok, health_reason = _provider_health_check(spec)
        if not ok:
            telemetry["failures"].append({"provider": spec.name, "reason": health_reason})
            continue

        try:
            state["llm_raw_output"] = _call_with_retry(spec, state["prompt_text"])
            telemetry["selected_provider"] = spec.name
            state["telemetry"] = telemetry
            return state
        except Exception as exc:  # noqa: BLE001
            telemetry["failures"].append({"provider": spec.name, "reason": _sanitize_error(exc)})
            continue

    telemetry["fallback"] = True
    fallback_json = {
        "analysis_summary": (
            f"Analyze: {state['job_title']}. Priorities: {state['guideline_text']}. "
            f"Tone hint: {state['tone_hint']}. {state['preference_note']}"
        ).strip(),
        "draft_text": _fallback_draft_by_structure(state),
    }
    state["llm_raw_output"] = json.dumps(fallback_json)
    state["telemetry"] = telemetry
    return state


def _parse_output(state: CoverLetterState) -> CoverLetterState:
    parse_error = None
    try:
        payload = json.loads(state["llm_raw_output"])
        parsed = LLMOutputSchema.model_validate(payload)
        state["analysis_summary"] = parsed.analysis_summary.strip()
        state["draft_text"] = parsed.draft_text.strip()
    except (json.JSONDecodeError, ValidationError, TypeError) as exc:
        parse_error = _sanitize_error(exc)
        state["analysis_summary"] = f"Analyze: {state['job_title']}"
        state["draft_text"] = _fallback_draft_by_structure(state)

    if not state["analysis_summary"]:
        state["analysis_summary"] = f"Analyze: {state['job_title']}"
    if not state["draft_text"]:
        state["draft_text"] = _fallback_draft_by_structure(state)

    if parse_error:
        state.setdefault("telemetry", {})
        state["telemetry"]["parser_recovery"] = True
        state["telemetry"]["parser_reason"] = parse_error
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


def run_cover_letter_graph(*, job_title: str, raw_text: str, headline: str, guideline_text: str, tone_hint: str, preference_note: str, structure: str) -> dict[str, Any]:
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
        "telemetry": {},
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

    return {
        "analysis_summary": result["analysis_summary"],
        "draft_text": result["draft_text"],
        "telemetry": result.get("telemetry", {}),
    }
