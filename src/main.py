from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.checks.log_check import run_log_check
from src.checks.service_check import run_service_check
from src.checks.config_check import run_config_check
from src.utils.io import write_json
from src.llm.summarizer import summarize_results



def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = repo_root / "outputs" / ts

    # -----------------------
    # 1) Log Check
    # -----------------------
    log_path = repo_root / "data" / "logs" / "sample_auth.log"
    log_result = run_log_check(log_path)
    write_json(out_dir / "results_log_check.json", log_result)

    print(f"[OK] Wrote: {out_dir / 'results_log_check.json'}")
    print(
        f"[STATUS] {log_result['status']} | "
        f"errors={log_result['summary']['level_counts'].get('ERROR', 0)} "
        f"warns={log_result['summary']['level_counts'].get('WARN', 0)}"
    )

    # -----------------------
    # 2) Service Health Check
    # -----------------------
    services_path = repo_root / "data" / "simulated_config" / "services.json"
    service_result = run_service_check(services_path)
    write_json(out_dir / "results_service_check.json", service_result)

    print(f"[OK] Wrote: {out_dir / 'results_service_check.json'}")
    print(
        f"[STATUS] {service_result['status']} | "
        f"stopped={service_result['summary']['status_counts'].get('stopped', 0)} "
        f"degraded={service_result['summary']['status_counts'].get('degraded', 0)}"
    )

    # -----------------------
    # 3) Config Validation Check
    # -----------------------
    config_path = repo_root / "data" / "simulated_config" / "app_config.json"
    config_result = run_config_check(config_path)
    write_json(out_dir / "results_config_check.json", config_result)

    print(f"[OK] Wrote: {out_dir / 'results_config_check.json'}")
    print(
        f"[STATUS] {config_result['status']} | "
        f"missing={len(config_result['summary']['missing_keys'])} "
        f"invalid={len(config_result['summary']['invalid_values'])} "
        f"warnings={len(config_result['summary']['warnings'])}"
    )

    # -----------------------
    # 4) AI Summary (Safe)
    # -----------------------
    all_results = {
    "log_check": log_result,
    "service_check": service_result,
    "config_check": config_result,
}

    ai_summary = summarize_results(all_results)
    write_json(out_dir / "results_ai_summary.json", ai_summary)

    print(f"[OK] Wrote: {out_dir / 'results_ai_summary.json'}")
    print("[INFO] AI summary generated (no inference, summarization only).")


if __name__ == "__main__":
    main()
