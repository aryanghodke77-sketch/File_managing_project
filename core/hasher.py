import os
import hashlib
from typing import List, Dict


def hash_file(file_path: str, chunk_size: int = 65536) -> str:
    """Return the SHA‑256 hash of the file at *file_path*.
    
    The file is read in *chunk_size* byte blocks to keep memory usage low.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_hashes(file_list: List[str], root_path: str) -> Dict[str, str]:
    """Create a mapping of relative file path → SHA‑256 hash.
    
    *file_list* should contain paths relative to *root_path* (as produced by
    ``scanner.scan_directory``). The function resolves each to an absolute path,
    hashes the file content, and returns a dictionary.
    """
    root_abs = os.path.abspath(root_path)
    hash_map: Dict[str, str] = {}
    for rel_path in file_list:
        abs_path = os.path.join(root_abs, rel_path)
        try:
            hash_map[rel_path] = hash_file(abs_path)
        except (OSError, PermissionError) as e:
            # For the beginner version we simply print a warning and skip the file.
            print(f"[hasher] Cannot read {rel_path}: {e}")
    return hash_map
