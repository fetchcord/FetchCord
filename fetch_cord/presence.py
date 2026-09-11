"""Building the Discord Rich Presence activity payload.

The mapping from fetched system info to the presence activity sent to Discord
is kept as a pure function so it can be unit-tested exhaustively without a
Discord connection (or any real hardware).
"""

from typing import Any

from fetch_cord.constants import RESULT_NOT_FOUND, UNKNOWN_COMPONENT_ID

# Values that mean "we could not work this out", rather than something worth
# putting on somebody's profile.
_PLACEHOLDERS = (None, "", RESULT_NOT_FOUND, UNKNOWN_COMPONENT_ID)


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
