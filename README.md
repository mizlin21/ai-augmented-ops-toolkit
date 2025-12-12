# AI-Augmented System Operations Toolkit

A lightweight, enterprise-style operations toolkit that runs common system checks (logs, service health, config validation), outputs structured results (JSON), and generates an AI-assisted summary for faster human triage.

## Why this exists
In real operations, engineers don’t have time to manually parse logs, cross-check service states, and validate configs during incidents. This toolkit simulates that workflow and shows how automation + safe AI summarization can reduce time-to-understand without hiding raw evidence.

## What it does (MVP)
- Log Check: parses log files and extracts warnings/errors + top issues
- Service Health Check: evaluates simulated service status data
- Config Validation: validates required configuration keys and safe values
- Outputs machine-readable results (JSON) + a human-friendly AI summary

# AI-Augmented System Operations Toolkit

A lightweight, enterprise-style operations toolkit that runs common system checks (logs, service health, config validation), outputs structured results (JSON), and generates an AI-assisted summary for faster human triage.

## Why this exists
In real operations, engineers don’t have time to manually parse logs, cross-check service states, and validate configs during incidents. This toolkit simulates that workflow and shows how automation + safe AI summarization can reduce time-to-understand without hiding raw evidence.

## Features (MVP)
- ✅ Log Check (parse auth/app logs; detect warnings/errors; extract top issues)
- ✅ Service Health Check (simulated service states via JSON)
- ✅ Config Validation (required keys + safe values)
- ✅ Structured outputs: JSON result bundle per run
- ✅ AI Summary layer: converts results → human-readable triage notes (with guardrails)

## Project Structure
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
outputs/
scripts/
run_all.sh
docs/
ARCHITECTURE.md
tests/


## How to Run (coming Day 3)
- Run all checks
- Save outputs to ./outputs/<timestamp>/
- Generate AI summary

## Safety / Guardrails (coming Day 4)
- Never invents metrics not present in JSON results
- Marks unknowns clearly
- Keeps raw evidence visible for human verification

## Why this matters for IBM
This project demonstrates:
- Systems thinking (design-first approach, repeatable checks, structured outputs)
- Automation mindset (Python + operational glue)
- Responsible AI integration (summarization with constraints)
- Clear documentation and “operator-friendly” tooling

## Roadmap
- Day 2: Implement core Python checks
- Day 3: Add orchestration scripts + CLI usage
- Day 4: Add AI summarizer + safety constraints
- Day 5: Polish + architecture diagram + IBM framing

## Example Output (coming soon)
- outputs/2025-xx-xx_1200/results.json
- outputs/2025-xx-xx_1200/ai_summary.md
