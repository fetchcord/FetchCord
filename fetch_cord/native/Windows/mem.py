"""Memory use, matching the format the PowerShell command produces.

e.g. "12.40 GB / 31.92 GB"

Used is total minus available, which is how the Linux and macOS commands
define it too, so the value stays comparable across platforms.
"""

import psutil

GIB = 1024**3


def fetch() -> str | None:
    try:
        memory = psutil.virtual_memory()
    except Exception:
        return None

    if not memory.total:
        return None

    used = memory.total - memory.available

    return f"{used / GIB:.2f} GB / {memory.total / GIB:.2f} GB"
