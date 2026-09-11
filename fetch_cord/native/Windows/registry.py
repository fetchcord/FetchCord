"""Small helpers for reading the Windows registry.

Every native Windows fetcher reads from here rather than shelling out, so the
whole native path stays free of subprocesses and of any external tool.
"""

import contextlib
import sys
from typing import TYPE_CHECKING

# Importable on any platform so the fetchers - and their tests - can be
# imported off Windows; every read simply reports None there. The TYPE_CHECKING
# arm keeps winreg visible to mypy when it runs on a non-Windows host.
if sys.platform == "win32" or TYPE_CHECKING:
    import winreg

# Where the values the fetchers need live.
CURRENT_VERSION = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
BIOS = "HARDWARE\\DESCRIPTION\\System\\BIOS"
CPU0 = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0"


def read(path: str, name: str) -> str | None:
    """Read one HKEY_LOCAL_MACHINE value, or None if it is not there.

    A missing key or value is an expected outcome - hardware varies and values
    come and go between Windows releases - so it is reported as None and the
    next provider fills the gap.
    """
    if sys.platform != "win32":
        return None

    # Read the 64-bit view explicitly: a 32-bit Python would otherwise be
    # redirected to WOW6432Node and see a different (or missing) ProductName.
    access = winreg.KEY_READ | winreg.KEY_WOW64_64KEY

    with (
        contextlib.suppress(OSError),
        winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, access) as key,
    ):
        value = winreg.QueryValueEx(key, name)[0]
        return str(value) if value != "" else None

    return None


def read_int(path: str, name: str) -> int | None:
    """Read one registry value as an int, or None if it is absent or not numeric."""
    value = read(path, name)
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None
