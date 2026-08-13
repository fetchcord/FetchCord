"""Structured parsing of fastfetch's `--format json` output.

fastfetch prints a JSON array where each element is either
`{"type": "ModuleName", "result": {...}}` or, on failure,
`{"type": "ModuleName", "error": "..."}`.

This module turns that into a flat `{field: display_string}` mapping, which is
what FetchCord renders into Rich Presence. Parsing structured data once is far
more robust than running `fastfetch | grep "Label"` for every field.
"""

import json
from typing import Any

# Modules we want fastfetch to emit, in display order.
FASTFETCH_MODULES = [
    "OS",
    "Kernel",
    "CPU",
    "GPU",
    "Memory",
    "Packages",
    "Shell",
    "Terminal",
    "Font",
]


def _first_text(result: dict[str, Any]) -> str:
    """Extract a human-readable string from an arbitrary module result."""
    for key in ("prettyName", "name", "exeName", "cpu", "value", "model", "product"):
        value = result.get(key)
        if isinstance(value, str) and value:
            return value
    for value in result.values():
        if isinstance(value, str) and value:
            return value
    return ""


def _format_module(module_type: str, result: dict[str, Any]) -> str:
    """Render one fastfetch module result as a display string."""
    if module_type == "OS":
        return result.get("prettyName") or result.get("name") or ""

    if module_type == "Kernel":
        return result.get("release") or result.get("name") or ""

    if module_type == "CPU":
        return result.get("cpu") or _first_text(result)

    if module_type == "Memory":
        used = int(result.get("used") or 0)
        total = int(result.get("total") or 0)
        return f"{used / 1024**3:.2f} GB / {total / 1024**3:.2f} GB"

    if module_type == "Packages":
        return str(result.get("all", ""))

    return _first_text(result)


def parse_fastfetch_json(raw: str) -> dict[str, str]:
    """Parse `fastfetch --format json` output into {field: display_string}.

    Unknown/errored modules and unrecognised JSON are silently skipped so a
    missing optional module never takes down Rich Presence.
    """
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}

    fields: dict[str, str] = {}
    if not isinstance(data, list):
        return fields

    for entry in data:
        if not isinstance(entry, dict):
            continue
        module_type = entry.get("type", "")
        if not isinstance(module_type, str) or "error" in entry:
            continue
        result = entry.get("result")
        if not isinstance(result, dict):
            continue

        value = _format_module(module_type, result)
        if value:
            fields[module_type.lower()] = value

    return fields
