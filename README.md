# File Integrity Monitoring (FIM) Project

A simple, modular Python tool that tracks changes to files in a directory.  
It can create a **baseline** snapshot of file hashes and later **compare** the current state to detect:

- Added files
- Modified files
- Deleted files
- Unchanged files

The code is deliberately kept beginner‑friendly: only the Python standard library is used, each module has a single responsibility, and the CLI is easy to invoke.

## Project Structure

## Project Structure

```text
file_integrity_monitor/
├── monitor.py              # CLI entry point & orchestrator
├── core/
│   ├── scanner.py          # Recursively discovers files (relative paths)
│   ├── hasher.py           # Computes SHA-256 hashes (chunked reading)
│   ├── storage.py          # Saves/loads the baseline JSON file
│   ├── comparer.py         # Diff logic (added / modified / deleted / unchanged)
│   └── reporter.py         # Formats and prints the diff, optional JSON report
├── data/
│   └── baseline.json       # Persisted baseline (created by the tool)
├── reports/                # Timestamped JSON reports from check
└── README.md
```


## How It Works (Data Flow)

1. **Baseline creation** (`monitor.py baseline <path>`):
   - `scanner` → list of relative file paths  
   - `hasher` → `{path: hash}` dictionary  
   - `storage` → writes `data/baseline.json`  

2. **Integrity check** (`monitor.py check <path>`):
   - `scanner` → current file list  
   - `hasher` → current hashes  
   - `storage` → loads saved baseline  
   - `comparer` → diff dictionary (`added`, `modified`, `deleted`, `unchanged`)  
   - `reporter` → prints a readable report and optionally writes a JSON file under `reports/`

## Getting Started

### Prerequisites

- Python 3.8+ (standard library only)
- No external dependencies

### Run the tool

```bash
# From the project root
python monitor.py baseline path/to/your/folder
# → creates a baseline.json and reports how many files were recorded

python monitor.py check path/to/your/folder
# → prints added/modified/deleted/unchanged counts and file lists
#   also writes a timestamped JSON report under ./reports/
```

### Example

```bash
# Create baseline
python monitor.py baseline test_folder
# Output: Baseline saved for 'C:\…\test_folder'. 2 files recorded.

# Modify a file, add a new one, then run check
python monitor.py check test_folder
# Output (example):
# Added: 1
#   new_file.txt
# Modified: 1
#   file1.txt
# Deleted: 0
# Unchanged: 1
#   sub\file2.txt
#
# Report written to: reports/report_20260625_151200.json
```

## Contributing / Extending

- **Add features**: e.g., hash algorithms, ignore patterns, richer reporting.  
- **Keep responsibilities clear**: each new feature should belong to a single module (e.g., a new `filter.py` for ignore rules).  
- **Testing**: the design makes it easy to unit‑test each module in isolation.

## License

This is a learning project – feel free to copy, modify, and experiment.

---
