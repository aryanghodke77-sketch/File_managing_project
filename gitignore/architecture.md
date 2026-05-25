# System Architecture

```text
User
  ↓
CLI / Entry Point (monitor.py)
  ↓
Command Router
  ├── baseline command
  └── check command
       ↓
   Orchestrator
    ├── Scanner
    ├── Hasher
    ├── Storage
    ├── Comparer
    └── Reporter
```

---

# Core Idea

The system has one job:

```text
Capture file state now
+
Remember previous file state
+
Compare both
+
Report differences
```

That is the whole architecture.

---

# Main Modules

## 1. `monitor.py`

The entry point of the whole project.

It:

* reads the user command,
* decides whether to create a baseline or run a check,
* connects all other modules.

It should contain almost no business logic.

Think of it as the **traffic controller**.

---

## 2. `scanner.py`

Finds files in the target directory.

Responsibilities:

* walk through folders recursively,
* collect file paths,
* ignore unwanted files if needed,
* handle missing or inaccessible paths.

Output:

* a list of file paths.

This is the **discovery layer**.

---

## 3. `hasher.py`

Generates a fingerprint for each file.

Responsibilities:

* open each file safely,
* read file content,
* compute hash using `hashlib`,

Output:

* a mapping like:

```text
{
  "path/to/file.txt": "sha256hashvalue"
}
```

This is the **integrity layer**.

---

## 4. `storage.py`

Saves and loads the baseline.

Responsibilities:

* write file path → hash data to JSON,
* load old baseline from JSON,
* handle missing or corrupted baseline files.

This is the **memory layer** of the system.

Without this module, the system cannot compare against previous state.

---

## 5. `comparer.py`

Compares the current scan with the saved baseline.

Responsibilities:

* detect added files,
* detect modified files,
* detect deleted files,
* detect unchanged files.

Input:

* old hash map
* new hash map

Output:

* structured diff result.

This is the **decision engine**.

---

## 6. `reporter.py`

Turns comparison results into human-readable output.

Responsibilities:

* print clean terminal output,
* optionally save a report file,
* show timestamps and counts.

This is the **presentation layer**.

---

# Data Flow

## Baseline Creation Flow

```text
User runs baseline command
→ monitor.py
→ scanner.py finds files
→ hasher.py hashes files
→ storage.py saves baseline.json
→ reporter.py prints success message
```

---

## Integrity Check Flow

```text
User runs check command
→ monitor.py
→ scanner.py finds current files
→ hasher.py hashes current files
→ storage.py loads old baseline
→ comparer.py compares old vs new
→ reporter.py prints report
```

---

# Data Model

The main data structure can be this:

```python
{
    "file_path_1": "hash_1",
    "file_path_2": "hash_2",
    "file_path_3": "hash_3"
}
```

This structure is enough for a solid beginner version.

Later, you can extend it to store:

* file size,
* modified time,
* scan timestamp.

But do not add that at first unless needed.

---

# Suggested Folder Structure

```text
file_integrity_monitor/
│
├── monitor.py
├── core/
│   ├── scanner.py
│   ├── hasher.py
│   ├── storage.py
│   ├── comparer.py
│   └── reporter.py
│
├── data/
│   └── baseline.json
│
├── reports/
├── test_folder/
└── README.md
```

---

# Responsibility Boundaries

A strong architecture rule for this project:

* `scanner.py` only finds files.
* `hasher.py` only hashes files.
* `storage.py` only saves/loads data.
* `comparer.py` only compares states.
* `reporter.py` only displays results.
* `monitor.py` only coordinates everything.

That separation is what makes the project feel like a real backend system.

---

# Final Shape of the System

The final system should behave like this:

```text
1. User chooses a folder
2. System scans folder
3. System creates hashes
4. System stores or loads baseline
5. System compares states
6. System reports changes
```
