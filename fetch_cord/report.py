"""Building a hardware report to paste into a GitHub issue.

Unrecognised hardware is the most common thing people open issues about, and
the id tables are this project's main upkeep. This turns "my motherboard shows
as unknown" into one command whose output already contains everything needed
to add an entry: the raw detected string to write a pattern against, and which
component actually missed.
"""

import platform

from fetch_cord import VERSION
from fetch_cord.constants import RESULT_NOT_FOUND
from fetch_cord.fetch import resolve_component_id

# Display name for each component that has an id table, keyed by the snapshot
# field, which is also how __main__ keys fetchcord_ids.
COMPONENTS: tuple[tuple[str, str], ...] = (
    ("OS", "os"),
    ("CPU", "cpu"),
    ("GPU", "gpu"),
    ("Motherboard", "motherboard"),
    ("Terminal", "terminal"),
    ("Shell", "shell"),
    ("System type", "system_type"),
)

# Fields used as cycle app_id values are lowercased before lookup in
# resolve_cycle; match that so the report can never disagree with what the
# presence actually did. Icon lookups (gpu/shell/system_type) stay as-is.
LOWERCASED = ("os", "cpu", "motherboard", "terminal")

MATCHED = "ok"
GENERIC = "**no match - needs an entry**"
NOT_DETECTED = "not detected on this machine"
NO_TABLE = "no id table loaded"


def _row(component: str, detected: str, matched: str, status: str) -> str:
    return f"| {component} | {detected or '-'} | {matched or '-'} | {status} |"


def build(
    snapshot: dict[str, str],
    fetchcord_ids: dict[str, dict[str, list[str]]],
) -> tuple[str, int]:
    """Render the report and return it with the number of unmatched components."""
    rows = []
    missing = 0

    for title, field in COMPONENTS:
        detected = snapshot.get(field, "")
        if not detected or detected == RESULT_NOT_FOUND:
            rows.append(_row(title, "", "", NOT_DETECTED))
            continue

        ids = fetchcord_ids.get(field)
        if not ids:
            # Say so rather than dropping the row: a silently missing
            # component is exactly what this command exists to surface.
            rows.append(_row(title, detected, "", NO_TABLE))
            continue

        search = detected.lower() if field in LOWERCASED else detected
        component_id, matched = resolve_component_id(search, ids)

        rows.append(
            _row(title, detected, component_id, MATCHED if matched else GENERIC)
        )
        if not matched:
            missing += 1

    lines = [
        "<!-- Paste this into a FetchCord issue -->",
        "",
        f"**FetchCord** {VERSION} on **{platform.system()} {platform.release()}**",
        "",
        "| Component | Detected | Matched id | Status |",
        "| --- | --- | --- | --- |",
        *rows,
        "",
    ]

    if missing:
        lines.append(
            f"{missing} component(s) found no match. The **Detected** column is "
            "the raw string a new id-table pattern needs to match."
        )
    else:
        lines.append("Everything on this machine matched an id-table entry.")

    return "\n".join(lines), missing


def report(
    snapshot: dict[str, str],
    fetchcord_ids: dict[str, dict[str, list[str]]],
) -> int:
    """Print the report. Returns a process exit code."""
    text, _ = build(snapshot, fetchcord_ids)
    print(text)
    return 0
