"""Building the Discord Rich Presence activity payload.

The mapping from fetched system info to the presence activity sent to Discord
is kept as a pure function so it can be unit-tested exhaustively without a
Discord connection (or any real hardware).
"""

from typing import Any


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
    """
    return {
        "state": state,
        "details": details,
        "large_image": large_image,
        "large_text": large_text,
        "small_image": small_image,
        "small_text": small_text,
        "start": start,
    }
