import os
from typing import List


def scan_directory(root_path: str) -> List[str]:
    """
    Discover all files under the given root directory.
    
    Returns a sorted list of relative file paths (relative to root_path).
    Uses os.walk with followlinks=False to safely avoid recursive symlinks.
    """
    root_abs = os.path.abspath(root_path)
    
    if not os.path.isdir(root_abs):
        raise ValueError(f"'{root_path}' is not a valid directory")
    
    files = []
    
    for dirpath, dirnames, filenames in os.walk(root_abs, followlinks=False):
        for filename in filenames:
            abs_file_path = os.path.join(dirpath, filename)
            try:
                rel_path = os.path.relpath(abs_file_path, root_abs)
                files.append(rel_path)
            except (PermissionError, OSError) as e:
                print(f"[scanner] Skipping file: {abs_file_path}")
    
    return sorted(files)