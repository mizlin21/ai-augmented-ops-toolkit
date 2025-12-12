# Architecture — AI-Augmented System Operations Toolkit

## Design Principles
- Deterministic checks first (auditable, repeatable)
- Structured evidence output (JSON)
- AI is advisory only (summarization, read-only)
- Each run is traceable (timestamped outputs)

## Data Flow Diagram

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
| Orchestration (src/main.py)|
+----------------------------+
   |         |          |
   v         v          v
Log Check  Service    Config
(src/checks) Check     Check
   |         |          |
   +---------+----------+
             |
             v
     JSON Evidence Outputs
 (outputs/<timestamp>/results_*.json)
             |
             v
     AI Summary (src/llm)
   summarize_results(read-only)
             |
             v
 outputs/<timestamp>/results_ai_summary.json
