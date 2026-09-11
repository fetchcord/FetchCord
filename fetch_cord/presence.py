"""Building the Discord Rich Presence activity payload.

The mapping from fetched system info to the presence activity sent to Discord
is kept as a pure function so it can be unit-tested exhaustively without a
Discord connection (or any real hardware).
"""

from dataclasses import dataclass
from typing import Any

from fetch_cord.constants import (
    MAX_BUTTON_LABEL,
    MAX_BUTTONS,
    RESULT_NOT_FOUND,
    UNKNOWN_COMPONENT_ID,
)
from fetch_cord.fetch import get_component_id

# Values that mean "we could not work this out", rather than something worth
# putting on somebody's profile.
_PLACEHOLDERS = (None, "", RESULT_NOT_FOUND, UNKNOWN_COMPONENT_ID)

DEFAULT_LARGE_IMAGE = "big"


@dataclass(frozen=True)
class ResolvedCycle:
    """One cycle's display values, resolved from a single snapshot.

    Kept separate from sending so the same resolution feeds the presence
    loop, ``--dry-run`` and ``scripts/validate.py`` - a dry run is only worth
    anything if it builds what the real loop would build.
    """

    name: str
    client_id: str
    app: str
    top: str
    bottom: str
    icon: str
    icon_id: str
    large_image: str

    def activity(self, start: int) -> dict[str, Any]:
        return build_presence_activity(
            details=self.top,
            state=self.bottom,
            large_image=self.large_image,
            large_text=self.app,
            small_image=self.icon_id,
            small_text=self.icon,
            start=start,
        )


def resolve_cycle(
    snapshot: dict[str, str],
    fetchcord_ids: dict[str, dict[str, list[str]]],
    *,
    name: str,
    app_id: str,
    top_line: str,
    bottom_line: str,
    small_icon: str,
) -> ResolvedCycle:
    """Map a snapshot onto one cycle's Discord app and display lines."""
    app = snapshot.get(app_id, RESULT_NOT_FOUND)
    top = snapshot.get(top_line, RESULT_NOT_FOUND)
    bottom = snapshot.get(bottom_line, RESULT_NOT_FOUND)
    icon = snapshot.get(small_icon, RESULT_NOT_FOUND)

    large_image = DEFAULT_LARGE_IMAGE
    # Apple silicon has a per-chip large image rather than the shared one.
    if icon and "apple m" in icon.lower():
        large_image = icon.lower().replace(" ", "-")

    return ResolvedCycle(
        name=name,
        client_id=get_component_id(app.lower(), fetchcord_ids[app_id]),
        app=app,
        top=top,
        bottom=bottom,
        icon=icon,
        icon_id=get_component_id(icon, fetchcord_ids[small_icon]),
        large_image=large_image,
    )


def parse_buttons(raw: Any) -> list[dict[str, str]]:
    """Validate configured profile buttons, dropping any Discord would reject.

    A bad button is worth a warning and a skip, never a crash: it would
    otherwise take the whole presence down over a typo in a config file.
    """
    if not raw:
        return []
    if not isinstance(raw, list):
        print("Warning: buttons must be a list, ignoring")
        return []

    buttons: list[dict[str, str]] = []
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            print(f"Warning: button {index} must be a mapping, ignoring")
            continue

        label = str(entry.get("label", "")).strip()
        url = str(entry.get("url", "")).strip()

        if not label or not url:
            print(f"Warning: button {index} needs both a label and a url, ignoring")
            continue
        if len(label) > MAX_BUTTON_LABEL:
            print(
                f"Warning: button {index} label is longer than "
                f"{MAX_BUTTON_LABEL} characters, ignoring"
            )
            continue
        # Discord only accepts https links on presence buttons.
        if not url.lower().startswith("https://"):
            print(f'Warning: button {index} url must start with "https://", ignoring')
            continue

        buttons.append({"label": label, "url": url})

    if len(buttons) > MAX_BUTTONS:
        print(
            f"Warning: Discord shows at most {MAX_BUTTONS} buttons, dropping the rest"
        )
        buttons = buttons[:MAX_BUTTONS]

    return buttons


def build_presence_activity(
    *,
    details: str,
    state: str,
    large_image: str,
    large_text: str,
    small_image: str,
    small_text: str,
    start: int,
    buttons: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Return the activity payload sent to Discord for a presence update.

    Mirrors the argument names pypresence's ``Presence.update()`` accepts, so
    the result can be splatted directly: ``self.rpc.update(**payload)``.

    ``small_image``/``small_text`` are dropped when they would only carry a
    placeholder: ``small_text`` is the tooltip for the small icon, so without
    an icon Discord has nothing to attach it to.
    """
    icon: str | None = small_image
    tooltip: str | None = small_text

    if icon in _PLACEHOLDERS:
        icon = None
        tooltip = None
    elif tooltip in _PLACEHOLDERS:
        tooltip = None

    payload: dict[str, Any] = {
        "state": state,
        "details": details,
        "large_image": large_image,
        "large_text": large_text,
        "small_image": icon,
        "small_text": tooltip,
        "start": start,
    }
    # Only sent when configured - pypresence rejects an empty list.
    if buttons:
        payload["buttons"] = buttons
    return payload
