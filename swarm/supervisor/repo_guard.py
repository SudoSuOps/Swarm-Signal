"""Repo Guard — enforces protected path policy.

Validates that patches do not touch locked system areas.
"""

PROTECTED_PATHS = ["core/", "contracts/", "tests/"]


def validate_patch(files_changed: list[str]) -> None:
    """Raise if any changed file falls inside a protected path."""
    for f in files_changed:
        for path in PROTECTED_PATHS:
            if f.startswith(path):
                raise Exception(f"Protected path modification detected: {f}")
