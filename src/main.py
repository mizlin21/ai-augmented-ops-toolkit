from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.checks.log_check import run_log_check
from src.utils.io import write_json


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    log_path = repo_root / "data" / "logs" / "sample_auth.log"
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = repo_root / "outputs" / ts

    result = run_log_check(log_path)
    write_json(out_dir / "results_log_check.json", result)

    print(f"[OK] Wrote: {out_dir / 'results_log_check.json'}")
    print(f"[STATUS] {result['status']} | errors={result['summary']['level_counts'].get('ERROR', 0)} "
          f"warns={result['summary']['level_counts'].get('WARN', 0)}")


if __name__ == "__main__":
    main()
