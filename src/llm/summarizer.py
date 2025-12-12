from __future__ import annotations

from typing import Dict, Any


SYSTEM_PROMPT = """
You are an enterprise system operations assistant.

Rules:
- Use ONLY the data provided.
- Do NOT invent metrics or events.
- Do NOT speculate.
- Do NOT assign blame.
- If information is missing, say so explicitly.
- Keep recommendations practical and conservative.
"""


def summarize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a human-readable summary from system check results.
    This function is intentionally deterministic and safe.
    """

    summaries = []

    for check_name, payload in results.items():
        status = payload.get("status", "UNKNOWN")
        findings = payload.get("findings", [])

        section = {
            "check": check_name,
            "status": status,
            "summary": _summarize_single_check(payload),
            "findings": findings,
        }

        summaries.append(section)

    return {
        "assistant": "ai_ops_summarizer",
        "rules": "summarization_only_no_inference",
        "summary": summaries,
    }


def _summarize_single_check(payload: Dict[str, Any]) -> str:
    status = payload.get("status", "UNKNOWN")

    if status == "PASS":
        return "No issues detected. System behavior is within expected parameters."

    if status == "WARN":
        return (
            "Potential issues detected. Review warnings to prevent "
            "possible degradation."
        )

    if status == "FAIL":
        return (
            "Critical issues detected. Immediate investigation is recommended "
            "to prevent service impact."
        )

    return "Status could not be determined from provided data."
