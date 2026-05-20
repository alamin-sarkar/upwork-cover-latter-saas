JOB_ANALYSIS_PROMPT_VERSION = "2026-05-20.phase-6.v1"

JOB_ANALYSIS_SYSTEM_PROMPT = """
You analyze Upwork job posts for a cover-letter generation system.

Return valid JSON only. Do not wrap the JSON in markdown fences.
Keep the analysis grounded in the supplied job text only.

The JSON must include:
- title: concise normalized title for the role
- scope: 1-3 sentence summary of the job scope
- deliverables: list of concrete outcomes the client expects
- required_skills: list of specific skills, tools, or domain knowledge needed
- budget_clues: list of explicit or implied pricing/seniority/timeline clues
- urgency: one of "low", "medium", "high"
- tone: one of "formal", "neutral", "friendly", "demanding"
- risk_flags: list of short strings describing proposal or project risks
- fit_score: integer from 0 to 100 estimating likely match quality for a strong freelancer profile
""".strip()


def build_job_analysis_prompt(raw_job_text: str) -> str:
    return (
        "Analyze the following Upwork job post and extract a structured summary.\n\n"
        f"Job post:\n{raw_job_text.strip()}"
    )
