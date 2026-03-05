"""Schema Validator
====================
Validates training pairs against contracts/pair.schema.json at runtime.
No external dependencies — reads the contract schema directly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONTRACTS_DIR = Path(__file__).resolve().parent.parent / "contracts"

_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "object": dict,
}


def load_schema(name: str = "pair.schema.json") -> dict[str, Any]:
    """Load a JSON schema from the contracts directory."""
    path = CONTRACTS_DIR / name
    return json.loads(path.read_text())


def validate_pair(pair: dict[str, Any]) -> list[str]:
    """Validate a single pair against pair.schema.json.

    Returns a list of error strings. Empty list means valid.
    """
    schema = load_schema("pair.schema.json")
    errors: list[str] = []

    # Required fields
    for field in schema.get("required", []):
        if field not in pair:
            errors.append(f"Missing required field: {field}")

    props = schema.get("properties", {})

    # Reject unknown fields if additionalProperties is false
    if schema.get("additionalProperties") is False:
        for field in pair:
            if field not in props:
                errors.append(f"Unexpected field: {field}")

    # Per-field validation
    for field, value in pair.items():
        if field not in props:
            continue
        spec = props[field]
        expected = spec.get("type")

        # Type check
        if expected and expected in _TYPE_MAP:
            if not isinstance(value, _TYPE_MAP[expected]):
                errors.append(
                    f"Field '{field}': expected {expected}, got {type(value).__name__}"
                )
                continue

        # String constraints
        if expected == "string" and isinstance(value, str):
            min_len = spec.get("minLength")
            if min_len is not None and len(value) < min_len:
                errors.append(f"Field '{field}': length {len(value)} < minLength {min_len}")

        # Number constraints
        if expected == "number" and isinstance(value, (int, float)):
            minimum = spec.get("minimum")
            maximum = spec.get("maximum")
            if minimum is not None and value < minimum:
                errors.append(f"Field '{field}': {value} < minimum {minimum}")
            if maximum is not None and value > maximum:
                errors.append(f"Field '{field}': {value} > maximum {maximum}")

    return errors


def is_valid_pair(pair: dict[str, Any]) -> bool:
    """Return True if the pair passes schema validation."""
    return len(validate_pair(pair)) == 0
