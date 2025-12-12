from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def run_service_check(services_path: Path) -> Dict[str, Any]:
    raw = services_path.read_text(encoding="utf-8", errors="replace")
    data = json.loads(raw)

    services: List[Dict[str, Any]] = data.get("services", [])
    normalized = []

    # Track counts for status logic
    counts = {"running": 0, "degraded": 0, "stopped": 0, "unknown": 0}

    for svc in services:
        name = str(svc.get("name", "unknown-service"))
        status = str(svc.get("status", "unknown")).lower().strip()

        if status not in ("running", "degraded", "stopped"):
            status = "unknown"

        counts[status] += 1
        normalized.append({"name": name, "status": status})

    # Decide PASS/WARN/FAIL
    status = "PASS"
    findings: List[str] = []

    if counts["stopped"] > 0:
        status = "FAIL"
        findings.append("One or more services are stopped.")
    elif counts["degraded"] > 0 or counts["unknown"] > 0:
        status = "WARN"
        if counts["degraded"] > 0:
            findings.append("One or more services are degraded.")
        if counts["unknown"] > 0:
            findings.append("One or more services have unknown status.")

    # Helpful lists for ops triage
    stopped = [s for s in normalized if s["status"] == "stopped"]
    degraded = [s for s in normalized if s["status"] == "degraded"]
    unknown = [s for s in normalized if s["status"] == "unknown"]

    return {
        "check": "service_check",
        "target": str(services_path),
        "status": status,
        "summary": {
            "total_services": len(normalized),
            "status_counts": counts,
            "stopped": stopped,
            "degraded": degraded,
            "unknown": unknown,
        },
        "findings": findings,
        "evidence_preview": normalized[:10],
    }
