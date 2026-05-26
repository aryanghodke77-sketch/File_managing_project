import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def _format_section(title: str, items: List[str]) -> str:
    """Return a formatted text block for a diff category.
    """
    lines = [f"{title}: {len(items)}"]
    lines.extend(f"  {p}" for p in items)
    return "\n".join(lines)


def print_report(diff: Dict[str, List[str]], target_path: str) -> None:
    """Display diff results and optionally write a JSON report.

    *Console output* – prints counts and file paths for each category.
    *JSON report* – saved under ``reports/`` with a timestamped filename.
    """
    # ----- console output -------------------------------------------------
    sections = [
        _format_section("Added", diff.get("added", [])),
        _format_section("Modified", diff.get("modified", [])),
        _format_section("Deleted", diff.get("deleted", [])),
        _format_section("Unchanged", diff.get("unchanged", [])),
    ]
    print("\n".join(sections))
    print("\nScan completed.\n")

    # ----- optional JSON report ------------------------------------------
    try:
        reports_dir = Path(__file__).resolve().parents[1] / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"report_{timestamp}.json"
        report_content = {
            "target": target_path,
            "timestamp": timestamp,
            "diff": diff,
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_content, f, indent=2, sort_keys=True)
        print(f"Report written to: {report_path}")
    except OSError as e:
        # Only catch filesystem‑related errors; other bugs should surface.
        print(f"[reporter] Warning – could not write report file: {e}")
