from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


REQUIRED_KEYS = ["env", "log_level", "max_login_attempts", "allowed_cidrs"]
ALLOWED_ENVS = {"dev", "test", "stage", "prod"}
ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARN", "ERROR"}


def _is_int_in_range(value: Any, min_v: int, max_v: int) -> bool:
    return isinstance(value, int) and min_v <= value <= max_v


def run_config_check(config_path: Path) -> Dict[str, Any]:
    raw = config_path.read_text(encoding="utf-8", errors="replace")
    cfg = json.loads(raw)

    missing: List[str] = []
    invalid: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    # 1) Required keys
    for k in REQUIRED_KEYS:
        if k not in cfg:
            missing.append(k)

    # If missing required keys, we can still continue validating what exists,
    # but status will be FAIL.
    env = str(cfg.get("env", "")).lower().strip()
    log_level = str(cfg.get("log_level", "")).upper().strip()
    max_attempts = cfg.get("max_login_attempts", None)
    allowed_cidrs = cfg.get("allowed_cidrs", None)

    # 2) Validate env
    if "env" in cfg and env not in ALLOWED_ENVS:
        invalid.append({"key": "env", "value": cfg.get("env"), "rule": f"must be one of {sorted(ALLOWED_ENVS)}"})

    # 3) Validate log level
    if "log_level" in cfg and log_level not in ALLOWED_LOG_LEVELS:
        invalid.append({"key": "log_level", "value": cfg.get("log_level"), "rule": f"must be one of {sorted(ALLOWED_LOG_LEVELS)}"})

    # 4) Validate max_login_attempts (security-relevant)
    if "max_login_attempts" in cfg:
        if not _is_int_in_range(max_attempts, 1, 10):
            invalid.append({"key": "max_login_attempts", "value": max_attempts, "rule": "must be an integer between 1 and 10"})
        else:
            # opinionated warning: high attempts increases brute-force exposure
            if max_attempts >= 8:
                warnings.append({"key": "max_login_attempts", "value": max_attempts, "note": "High value may increase brute-force risk (consider <= 5)"})

    # 5) Validate allowed_cidrs (basic type validation)
    if "allowed_cidrs" in cfg:
        if not isinstance(allowed_cidrs, list) or not all(isinstance(x, str) for x in allowed_cidrs):
            invalid.append({"key": "allowed_cidrs", "value": allowed_cidrs, "rule": "must be a list[str]"})
        else:
            # minimal guardrail warning: 0.0.0.0/0 is overly permissive
            if any(x.strip() == "0.0.0.0/0" for x in allowed_cidrs):
                warnings.append({"key": "allowed_cidrs", "value": allowed_cidrs, "note": "0.0.0.0/0 is overly permissive; restrict CIDRs"})

    # Determine status
    status = "PASS"
    findings: List[str] = []

    if missing:
        status = "FAIL"
        findings.append("Missing required configuration keys.")
    if invalid:
        status = "FAIL"
        findings.append("Invalid configuration values detected.")
    if status != "FAIL" and warnings:
        status = "WARN"
        findings.append("Configuration is valid but contains risk warnings.")

    return {
        "check": "config_check",
        "target": str(config_path),
        "status": status,
        "summary": {
            "required_keys": REQUIRED_KEYS,
            "missing_keys": missing,
            "invalid_values": invalid,
            "warnings": warnings,
        },
        "findings": findings,
        "evidence_preview": {k: cfg.get(k) for k in REQUIRED_KEYS if k in cfg},
    }
