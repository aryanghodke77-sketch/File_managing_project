from typing import Dict, List


def compare_baselines(old: Dict[str, str], new: Dict[str, str]) -> Dict[str, List[str]]:
    """Compare two baseline dictionaries and classify file changes.

    Returns a dictionary with four keys:
        * "added"      – files present only in *new*
        * "modified"   – files present in both but with different hashes
        * "deleted"    – files present only in *old*
        * "unchanged"  – files present in both with identical hashes
    Each value is a list of relative file paths.
    """
    old_set = set(old.keys())
    new_set = set(new.keys())

    added = list(new_set - old_set)
    deleted = list(old_set - new_set)

    # Files in both sets – need to check if hash changed
    intersect = old_set & new_set
    modified = [p for p in intersect if old[p] != new[p]]
    unchanged = [p for p in intersect if old[p] == new[p]]

    return {
        "added": sorted(added),
        "modified": sorted(modified),
        "deleted": sorted(deleted),
        "unchanged": sorted(unchanged),
    }
