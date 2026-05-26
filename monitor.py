import argparse
import sys
from pathlib import Path

from core.scanner import scan_directory
from core.hasher import generate_hashes
from core.storage import save_baseline, load_baseline
from core.comparer import compare_baselines
from core.reporter import print_report




def run_baseline(target: str) -> None:
    """Create a baseline for *target* directory and persist it.
    """
    files = scan_directory(target)
    hashes = generate_hashes(files, target)
    save_baseline(hashes)
    print(f"Baseline saved for '{target}'. {len(hashes)} files recorded.")


def run_check(target_path: str) -> None:
    """Compare current state of *target_path* against stored baseline.
    """
    old = load_baseline()
    if not old:
        print("No baseline found. Run the baseline command first.")
        sys.exit(1)

    files = scan_directory(target_path)
    new = generate_hashes(files, target_path)
    diff = compare_baselines(old, new)
    print_report(diff, target_path)


def main(argv: list | None = None) -> None:
    parser = argparse.ArgumentParser(prog="monitor", description="File Integrity Monitoring CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline_parser = subparsers.add_parser("baseline", help="Create a baseline snapshot")
    baseline_parser.add_argument("path", type=str, help="Target directory to scan")

    check_parser = subparsers.add_parser("check", help="Check current state against baseline")
    check_parser.add_argument("path", type=str, help="Target directory to scan")

    args = parser.parse_args(argv)

    # Normalize the path (resolve to absolute) – other modules expect a path string.
    target_path = str(Path(args.path).resolve())

    if args.command == "baseline":
        run_baseline(target_path)
    elif args.command == "check":
        run_check(target_path)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
