from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


LOG_PATTERN = re.compile(
    r"^(?P<ts>\S+)\s+(?P<level>INFO|WARN|ERROR)\s+(?P<source>\S+)\s+(?P<message>.+)$"
)

SEVERITY_SCORE = {"INFO": 1, "WARN": 5, "ERROR": 10}


def parse_log_lines(lines: List[str]) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue

        m = LOG_PATTERN.match(raw)
        if not m:
            # Keep evidence even if line doesn't match expected format
            events.append(
                {"raw": raw, "parse_ok": False, "level": "UNKNOWN", "severity": 0}
            )
            continue

        level = m.group("level")
        events.append(
            {
                "ts": m.group("ts"),
                "level": level,
                "source": m.group("source"),
                "message": m.group("message"),
                "parse_ok": True,
                "severity": SEVERITY_SCORE.get(level, 0),
            }
        )

    return events


def run_log_check(log_path: Path, top_n: int = 5) -> Dict[str, Any]:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    events = parse_log_lines(lines)

    level_counts = Counter(e.get("level", "UNKNOWN") for e in events)
    total_severity = sum(int(e.get("severity", 0)) for e in events)

    # Count "issue signatures" (simple: source + message)
    issue_signatures = Counter()
    for e in events:
        if e.get("level") in ("WARN", "ERROR"):
            sig = f"{e.get('source')} | {e.get('message')}"
            issue_signatures[sig] += 1

    top_issues = [
        {"issue": issue, "count": count} for issue, count in issue_signatures.most_common(top_n)
    ]

    findings = []
    if level_counts.get("ERROR", 0) > 0:
        findings.append("Errors detected in logs.")
    if level_counts.get("WARN", 0) >= 2:
        findings.append("Multiple warnings detected; investigate potential degradation.")
    if level_counts.get("UNKNOWN", 0) > 0:
        findings.append("Some log lines could not be parsed; review raw evidence.")

    status = "PASS"
    if level_counts.get("ERROR", 0) > 0:
        status = "FAIL"
    elif level_counts.get("WARN", 0) > 0:
        status = "WARN"

    return {
        "check": "log_check",
        "target": str(log_path),
        "status": status,
        "summary": {
            "total_lines": len(lines),
            "parsed_events": sum(1 for e in events if e.get("parse_ok")),
            "level_counts": dict(level_counts),
            "total_severity": total_severity,
            "top_issues": top_issues,
        },
        "findings": findings,
        "evidence_preview": events[:10],  # keep it small; full logs stay in file
    }
