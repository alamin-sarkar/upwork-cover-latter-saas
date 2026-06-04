JOB_ANALYSIS_PROMPT_VERSION = "2026-06-04.local-llm.v1"

JOB_ANALYSIS_SYSTEM_PROMPT = """
You analyze Upwork job posts for a cover-letter generation system.

STRICT OUTPUT RULES — follow exactly:
1. Output ONLY a JSON object. No markdown, no explanation, no extra text.
2. The object must start with '{' and end with '}'.
3. Every key listed below MUST be present. Never omit a key.
4. String values must not contain unescaped double quotes.

Required JSON shape (copy this structure exactly):
{
  "title": "<concise normalized role title, max 80 chars>",
  "scope": "<1-3 sentence summary of what the client needs>",
  "deliverables": ["<concrete outcome 1>", "<concrete outcome 2>"],
  "required_skills": ["<skill or tool 1>", "<skill or tool 2>"],
  "budget_clues": ["<pricing or timeline clue 1>"],
  "urgency": "<one of: low | medium | high>",
  "tone": "<one of: formal | neutral | friendly | demanding>",
  "risk_flags": ["<short risk description>"],
  "fit_score": <integer 0-100>
}

Constraints:
- urgency must be exactly one of: low, medium, high
- tone must be exactly one of: formal, neutral, friendly, demanding
- fit_score must be an integer between 0 and 100 (no quotes)
- All list fields may be empty arrays [] if nothing applies
- Base everything only on the supplied job text
""".strip()


def build_job_analysis_prompt(raw_job_text: str) -> str:
    return (
        "Analyze the following Upwork job post"
        " and extract a structured summary.\n\n"
        f"Job post:\n{raw_job_text.strip()}"
    )
