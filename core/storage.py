import os
import json
from typing import Dict

BASELINE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")
BASELINE_FILE = os.path.join(BASELINE_DIR, "baseline.json")


def _ensure_baseline_dir() -> None:
    """Create the baseline directory if it does not exist.
    
    The function is idempotent and does nothing when the directory already
    exists. It keeps storage responsibilities isolated from other modules.
    """
    os.makedirs(BASELINE_DIR, exist_ok=True)


def save_baseline(baseline: Dict[str, str]) -> None:
    """Persist the *baseline* mapping to ``data/baseline.json``.
    
    The function overwrites any existing file. Errors while writing are not
    silenced – they will raise an exception so the caller can react
    appropriately (e.g., report a failure to the user).
    """
    _ensure_baseline_dir()
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2, sort_keys=True)


def load_baseline() -> Dict[str, str]:
    """Load the previously saved baseline.
    
    Returns an empty dictionary when the file does not exist or is corrupted.
    Corruption is handled by catching ``json.JSONDecodeError`` and returning
    ``{}``. This keeps the system operational for a beginner scenario while
    still providing a clear signal that the baseline could not be read.
    """
    if not os.path.isfile(BASELINE_FILE):
        return {}
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            # If the JSON is not a dict, treat it as corrupted.
            return {}
    except (OSError, json.JSONDecodeError):
        return {}
