"""Noticing when another program should own the Rich Presence instead.

Discord shows one activity at a time, so while a game or Spotify is running
FetchCord's system info replaces the status the user actually wants to see.
``pause_when`` lists the programs that should win.
"""

from collections.abc import Iterable

import psutil


def _variants(name: str) -> set[str]:
    """A process name with and without its ``.exe`` suffix.

    Lets one config line ("steam") match on every platform.
    """
    name = name.strip().lower()
    if not name:
        return set()

    if name.endswith(".exe"):
        return {name, name[: -len(".exe")]}
    return {name, name + ".exe"}


def running_names() -> list[str]:
    """Lowercased names of every process we can see."""
    names: list[str] = []

    try:
        processes = psutil.process_iter(["name"])
    except psutil.Error:
        return []

    for process in processes:
        try:
            name = process.info.get("name")
        except (psutil.Error, KeyError):
            # A process exiting between listing and reading is normal and
            # must not abandon the whole scan.
            continue
        if name:
            names.append(name.lower())

    return names


def find_running(names: Iterable[str]) -> str | None:
    """The first of ``names`` currently running, as the caller spelled it."""
    wanted: dict[str, str] = {}
    for name in names:
        for variant in _variants(name):
            wanted[variant] = name.strip()

    if not wanted:
        return None

    for running in running_names():
        if running in wanted:
            return wanted[running]

    return None


class PauseWatcher:
    """Tracks which configured program is holding the presence back.

    Announces the transitions only. This is checked once per cycle, so a line
    every time would be noise.
    """

    def __init__(self, names: Iterable[str] | None = None) -> None:
        self.names = [name for name in (names or []) if name and name.strip()]
        self.paused_for: str | None = None

    def check(self) -> str | None:
        """The program currently pausing us, or None."""
        if not self.names:
            return None

        found = find_running(self.names)

        if found and found != self.paused_for:
            print(f"Pausing: {found} is running.")
        elif self.paused_for and not found:
            print(f"{self.paused_for} closed, resuming.")

        self.paused_for = found
        return found
