"""
LLM provider adapter.

Supports three backends controlled by settings.llm_provider:
  - "anthropic"  → Anthropic SDK (default, production-grade)
  - "ollama"     → Ollama local server  (OpenAI-compatible, default :11434)
  - "lmstudio"   → LM Studio local server (OpenAI-compatible, default :1234)

The adapter exposes two things that the rest of the app needs:
  1. raw_completion(messages, system) → str
     Used by job_analysis which does its own JSON parsing.
  2. langchain_chat_model() → BaseChatModel
     Used by the generation service via with_structured_output().
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Raw completion (used by job_analysis)
# ---------------------------------------------------------------------------

async def raw_completion(
    messages: list[dict[str, str]],
    *,
    system: str,
    max_tokens: int = 1200,
    settings: Any | None = None,
) -> str:
    """
    Call the configured LLM and return the text response.

    For local providers the function retries up to settings.local_llm_json_retries
    times, appending a stricter reminder on each retry so that models like Qwen
    eventually comply with the JSON-only requirement.
    """
    from app.core.config import get_settings
    cfg = settings or get_settings()

    if cfg.llm_provider == "anthropic":
        return await _anthropic_raw(messages, system=system, max_tokens=max_tokens, cfg=cfg)

    return await _openai_compat_raw(messages, system=system, max_tokens=max_tokens, cfg=cfg)


async def _anthropic_raw(
    messages: list[dict[str, str]],
    *,
    system: str,
    max_tokens: int,
    cfg: Any,
) -> str:
    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key=cfg.anthropic_api_key)
    response = await client.messages.create(
        model=cfg.anthropic_model,
        max_tokens=max_tokens,
        temperature=0,
        system=system,
        messages=messages,
    )
    parts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
    if not parts:
        raise ValueError("Anthropic response contained no text blocks")
    return "\n".join(parts).strip()


async def _openai_compat_raw(
    messages: list[dict[str, str]],
    *,
    system: str,
    max_tokens: int,
    cfg: Any,
) -> str:
    """
    OpenAI-compatible call (Ollama / LM Studio).

    Forces JSON output two ways:
    1. response_format={"type": "json_object"} — honoured by most local servers.
    2. System prompt injection — explicit JSON-only instruction as a hard constraint.
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        base_url=cfg.local_llm_base_url,
        api_key="local",          # Ollama/LM Studio ignore this but the SDK requires it
        timeout=120.0,
    )

    full_messages = [{"role": "system", "content": _local_system(system)}, *messages]

    last_err: Exception | None = None
    for attempt in range(cfg.local_llm_json_retries):
        try:
            response = await client.chat.completions.create(
                model=cfg.local_llm_model,
                messages=full_messages,
                max_tokens=max_tokens,
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            text = (response.choices[0].message.content or "").strip()
            # Validate it is parseable JSON before returning
            json.loads(text)
            return text
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            logger.warning(
                "Local LLM attempt %d/%d failed: %s",
                attempt + 1,
                cfg.local_llm_json_retries,
                exc,
            )
            # On retry, inject a stricter reminder as the last user turn
            reminder = {
                "role": "user",
                "content": (
                    "IMPORTANT: your previous response was not valid JSON. "
                    "Output ONLY a raw JSON object — no markdown, no explanation, no extra text. "
                    "Start your response with '{' and end with '}'."
                ),
            }
            if full_messages[-1].get("role") == "user" and full_messages[-1].get(
                "content", ""
            ).startswith("IMPORTANT:"):
                full_messages[-1] = reminder
            else:
                full_messages.append(reminder)

    raise ValueError(
        f"Local LLM did not return valid JSON after {cfg.local_llm_json_retries} attempts"
    ) from last_err


# ---------------------------------------------------------------------------
# LangChain chat model (used by generation service)
# ---------------------------------------------------------------------------

def langchain_chat_model(settings: Any | None = None):
    """
    Return a LangChain BaseChatModel for the configured provider.

    For local models we use ChatOpenAI pointed at the local server.
    with_structured_output is called by the caller; we configure it
    to use "json_mode" so it works on models without full JSON-schema support.
    """
    from app.core.config import get_settings
    cfg = settings or get_settings()

    if cfg.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=cfg.anthropic_model,
            api_key=cfg.anthropic_api_key,
            temperature=0,
        )

    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=cfg.local_llm_model,
        base_url=cfg.local_llm_base_url,
        api_key="local",
        temperature=0,
        max_tokens=2048,
        timeout=120,
        # Tell the server we want JSON — works on Ollama ≥0.1.34 and LM Studio ≥0.2.19
        model_kwargs={"response_format": {"type": "json_object"}},
    )


def structured_output_method(settings: Any | None = None) -> str:
    """
    Return the best with_structured_output() method for the active provider.

    Anthropic supports "json_schema" (strict).
    Local models only reliably support "json_mode" (best-effort).
    """
    from app.core.config import get_settings
    cfg = settings or get_settings()
    return "json_schema" if cfg.llm_provider == "anthropic" else "json_mode"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _local_system(base_system: str) -> str:
    """
    Prepend a hard JSON discipline block to any system prompt sent to a local model.
    Local models (Qwen, Mistral, etc.) need very explicit instruction to stay in JSON mode.
    """
    json_contract = (
        "## OUTPUT CONTRACT (read first, follow exactly)\n"
        "You MUST output ONLY a single raw JSON object.\n"
        "Rules:\n"
        "- Start with '{', end with '}'\n"
        "- No markdown fences (no ```json)\n"
        "- No explanation, preamble, or commentary outside the JSON\n"
        "- No trailing text after the closing '}'\n"
        "- All string values must be valid JSON strings (escape quotes)\n"
        "- If you are uncertain about a value, use a short placeholder string — "
        "never omit a required key\n"
        "Violating any rule causes a pipeline failure.\n\n"
    )
    return json_contract + base_system
