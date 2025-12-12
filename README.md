# AI-Augmented System Operations Toolkit

A lightweight, enterprise-style system operations toolkit that runs deterministic checks (log analysis, service health, configuration validation), produces structured evidence (JSON), and generates a **safe AI-assisted summary** for faster human triage.

This project demonstrates how **automation and responsible AI** can improve operational visibility **without replacing deterministic controls or hiding raw evidence**.

---

## Why This Exists

In real enterprise environments, operators often need to:
- parse logs under time pressure
- cross-check service states
- validate configuration safety
- communicate system health quickly and accurately

Manual inspection is:
- slow
- error-prone
- difficult to scale

This toolkit simulates a real operations workflow by:
- automating common checks
- preserving auditable evidence
- using AI **only** to summarize validated results

---

## What This Toolkit Does (MVP)

- ✅ **Log Analysis**
  - Parses log files
  - Extracts INFO / WARN / ERROR counts
  - Identifies top recurring issues
  - Preserves raw evidence

- ✅ **Service Health Check**
  - Evaluates simulated service states
  - Detects running, degraded, and stopped services
  - Produces clear PASS / WARN / FAIL status

- ✅ **Configuration Validation**
  - Validates required configuration keys
  - Enforces safe value ranges
  - Flags risky but non-fatal settings

- ✅ **Structured Outputs**
  - One JSON artifact per check
  - Timestamped output folders per run

- ✅ **AI Summary Layer (Safe by Design)**
  - Converts validated results into human-readable summaries
  - Uses strict guardrails (no inference, no mutation)

---

## How to Run

### Option 1 — Run Like an Operator (Recommended)
```powershell
.\scripts\run_all.ps1

``` 

### Option 2 — Run Directly with Python
```
 python -m src.main

``` 

---

## Output Artifacts

Each execution creates a timestamped folder:

outputs/<YYYY-MM-DD_HHMMSS>/


Containing:

results_log_check.json

results_service_check.json

results_config_check.json

results_ai_summary.json

Each file is independent, auditable, and machine-readable.

⚠️ Runtime outputs are environment-specific and are recommended to be ignored in git.

---

## Architecture Overview

This toolkit follows a deterministic-first, AI-assisted architecture.

### High-Level Flow
```text
Operator / Automation
        |
        v
scripts/run_all.ps1
        |
        v
python -m src.main
        |
        v
+----------------------------+
|   Orchestration (main.py)  |
+----------------------------+
   |         |          |
   v         v          v
Log Check  Service     Config
           Check       Check
   |         |          |
   +---------+----------+
             |
             v
     Structured JSON Evidence
             |
             v
        AI Summary Layer
        (Read-only, Safe)
             |
             v
  results_ai_summary.json
```
See detailed documentation in: docs/ARCHITECTURE.md

---

## AI Safety & Guardrails (Responsible AI)

The AI layer is advisory only.

**What the AI does**
- Reads structured JSON results
- Summarizes system health
- Improves human readability


#### What the AI does NOT do

- ❌ Execute commands
- ❌ Modify files or system state
- ❌ Override PASS / WARN / FAIL decisions
- ❌ Invent metrics or events
- ❌ Hide raw evidence

Source of truth remains deterministic checks.

This design aligns with enterprise AI governance, auditability, and compliance expectations.

---

## Project Structure
```
src/
  main.py
  checks/
    log_check.py
    service_check.py
    config_check.py
  llm/
    summarizer.py
  utils/
    io.py

data/
  logs/
    sample_auth.log
  simulated_config/
    services.json
    app_config.json

scripts/
  run_all.ps1

docs/
  ARCHITECTURE.md

tests/

outputs/        # runtime artifacts (recommended .gitignore)
```

---

## Why This Matters for IBM / Enterprise Roles

#### This project demonstrates:

- Systems thinking
- Design before implementation
- Clear separation of concerns
- Automation mindset
- Repeatable, operator-friendly execution
- Timestamped, auditable outputs
- Responsible AI integration
- AI as a communication layer, not a controller
- Guardrails that prevent hallucination and unsafe behavior
- Enterprise readiness
- Deterministic behavior
- Clear documentation
- Interview-ready architecture narrative

---

## Example Execution

Produces:

outputs/2025-12-12_151709/
  results_log_check.json
  results_service_check.json
  results_config_check.json
  results_ai_summary.json

---

## Roadmap (Optional Enhancements)

- Add Linux/macOS runner script
- Add exit codes based on overall health
- Add basic unit tests per check
- Add CI integration (GitHub Actions)
- Add SOC-style incident summary mode

---

## Final Note

This is **not** a demo or toy project.

It is a  **mini operations platform** designed to reflect:
- real enterprise workflows
- safe AI adoption
- professional engineering practices

---