"""Building the Discord Rich Presence activity payload.

The mapping from fetched system info to the presence activity sent to Discord
is kept as a pure function so it can be unit-tested exhaustively without a
Discord connection (or any real hardware).
"""

from dataclasses import dataclass
from typing import Any

from fetch_cord.constants import RESULT_NOT_FOUND, UNKNOWN_COMPONENT_ID
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


def build_presence_activity(
    *,
    details: str,
    state: str,
    large_image: str,
    large_text: str,
    small_image: str,
    small_text: str,
    start: int,
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

    return {
        "state": state,
        "details": details,
        "large_image": large_image,
        "large_text": large_text,
        "small_image": icon,
        "small_text": tooltip,
        "start": start,
    }
