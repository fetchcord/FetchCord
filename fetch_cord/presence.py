"""Building the Discord Rich Presence activity payload.

The mapping from fetched system info to the presence activity sent to Discord
is kept as a pure function so it can be unit-tested exhaustively without a
Discord connection (or any real hardware).
"""

from typing import Any

from fetch_cord.constants import MAX_BUTTON_LABEL, MAX_BUTTONS


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
    """
    payload: dict[str, Any] = {
        "state": state,
        "details": details,
        "large_image": large_image,
        "large_text": large_text,
        "small_image": small_image,
        "small_text": small_text,
        "start": start,
    }
    # Only sent when configured - pypresence rejects an empty list.
    if buttons:
        payload["buttons"] = buttons
    return payload
